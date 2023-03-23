from PyQt5.QtCore import QRunnable, Qt, QThreadPool, pyqtSignal, QObject
from can import Message
import os
import can
import time

# https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/
# https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup#method-2-autostart

PROCESS_FAKE_MSG = True
fake_msg_num = 0

# analog update time to 20, improve efficiency

if not PROCESS_FAKE_MSG:
    os.system('sudo ip link set can0 type can bitrate 500000')
    os.system('sudo ifconfig can0 up')
    can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

# https://www.aemelectronics.com/sites/default/files/aem_product_instructions/Infinity-ECU-Full-Manual.pdf
# https://www.pragmaticlinux.com/2021/10/can-communication-on-the-raspberry-pi-with-socketcan/
# https://www.waveshare.com/w/upload/2/29/RS485-CAN-HAT-user-manuakl-en.pdf
# https://forums.raspberrypi.com/viewtopic.php?t=141052
# https://harrisonsand.com/posts/can-on-the-raspberry-pi/

TIMEOUT = 10
MSGID_0 = 0x01F0A000
MSGID_3 = 0x01F0A003
MSGID_4 = 0x01F0A004
MSGID_5 = 0x01F0A005
MSGID_6 = 0x01F0A006
MAX_BLUR_THROTTLE = 50  # percent throttle at which blur reaches max effect


def unsigned_int_to_signed8(i):
    return i if i < 128 else i - 256

def c_to_f(c):
    return c * 1.8 + 32


class Receive(QRunnable):
    class SignalHelper(QObject):
        update_data = pyqtSignal(float, dict)
        set_timestamp = pyqtSignal(float)
        log_msg = pyqtSignal(str)
        log_text = pyqtSignal(int, str)
    signals = SignalHelper()

    def __init__(self):
        super(Receive, self).__init__()
        self.keep_running = True

    def run(self):
        while self.keep_running:
            if PROCESS_FAKE_MSG:
                time.sleep(0.001)
                msg = test_msgid0()
            else:
                msg = can0.recv(TIMEOUT)
            if msg is not None:
                self.signals.set_timestamp.emit(msg.timestamp)
                self.parse_message(msg.arbitration_id, msg.timestamp, msg.data)
                self.signals.log_msg.emit(str(msg))

    def stop(self):
        self.keep_running = False
        if not PROCESS_FAKE_MSG:
            os.system('sudo ifconfig can0 down')

    def parse_message(self, id, timestamp, data):
        data_dict = {}
        if id == MSGID_0:
            # byte 0-1, Engine Speed, 16 bit unsigned, scaling 0.39063 rpm/bit, range 0 to 25,599.94 RPM
            data_dict['engine_speed'] = (data[0] * 256 + data[1]) * 0.39063 / 1000
            # byte 4-5, Throttle, 16 bit unsigned, scaling 0.0015259 %/bit, range 0 to 99.998 %
            data_dict['throttle'] = (data[4] * 256 + data[5]) * 0.0015259
            # byte 6, Intake Air Temp, 8 bit signed 2's comp, 1 Deg C/bit, -128 to 127 C
            data_dict['intake'] = c_to_f(unsigned_int_to_signed8(data[6]))
            # byte 7, Coolant Temp,  8 bit signed 2's comp, scaling 1 Deg C/bit, range -128 to 127 C
            data_dict['coolant'] = c_to_f(unsigned_int_to_signed8(data[7]))
        elif id == MSGID_3:
            # byte 0, Lambda #1, 8 bit unsigned, scaling 0.00390625 Lambda/bit, offset 0.5, range 0.5 to 1.496 Lambda
            data_dict['lambda1'] = data[0] * 0.00390625 + 0.5
            # byte 2-3, Vehicle Speed, 16 bit unsigned, scaling 0.0062865 kph/bit, range 0 to 411.986 km/h
            data_dict['vehicle_speed'] = (data[2] * 256 + data[3]) * 0.0062865
            # byte 4, Gear Calculated, 8 bit unsigned, 0 to 255
            data_dict['gear'] = data[4]
            # byte 5, Ign Timing, 8 bit unsigned, scaling .35156 Deg/bit, offset -17, range -17 to 72.65Deg
            data_dict['ignition_timing'] = data[5] * 0.35156 - 17
            # byte 6-7, Battery Volts, 16 bit unsigned, 0.0002455 V/bit, 0 to 16.089 Volts
            data_dict['battery'] = (data[6] * 256 + data[7]) * 0.0002455
        elif id == MSGID_4:
            # byte 0-1, Manifold Absolute Pressure, 16 bit unsigned, 0.1 kPa/bit, 0 to 6,553.5 kPa
            data_dict['map'] = (data[0] * 256 + data[1]) * 0.1
            # byte 2, Volumetric Efficiency, 8 bit unsigned, 1 %/bit, 0 to 255 %
            data_dict['ve'] = data[2]
            # byte 3, Fuel Pressure, 8 bit unsigned, 0.580151 PSIg/bit, 0 to 147.939 PSIg
            data_dict['fuel_pressure'] = data[3] * 0.580151
            # byte 5, Lambda Target, 8 bit unsigned, 0.00390625 Lambda/bit, offset 0.5, 0.5 to 1.496 Lambda
            data_dict['lambda_target'] = data[5] * 0.00390625 + 0.5
            # byte 6
            byte6_bin = "{:08b}".format(data[6])
            # bit 0 (lsb), FuelPump, Boolean 0 = false, 1 = true, 0, 0/1
            data_dict['fuel_pump'] = int(byte6_bin[7])
            # bit 1 Fan 1 Boolean 0 = false, 1 = true 0 0/1
            data_dict['fan1'] = int(byte6_bin[6])
        elif id == MSGID_5:
            # byte 0-1, Launch Ramp Time [ms], 16 bit unsigned, 10 mS/bit, 0 to 655,350 mS
            data_dict['lrt'] = (data[0] * 256 + data[1]) * 10
            # byte 2-3, Mass Airflow [gms/s], 16 bit unsigned, .05 [gms/s] / bit, 0 to 3,276.75 gms/s
            data_dict['mass_airflow'] = (data[2] * 256 + data[3]) * 0.05
        elif id == MSGID_5:
            # byte 2, PrimaryInjDuty [%], 8 bit unsigned, 0.392157 %/bit, 0 to 100 %
            data_dict['injector_duty'] = data[2] * 0.392157
        else:
            data_dict['unk'] = 0
        self.signals.update_data.emit(timestamp, data_dict)


def test_msgid0():
    global fake_msg_num
    fake_msg_num = min(fake_msg_num + 0.1, 255)
    return Message(data=bytearray([int(fake_msg_num), 0, 0, 0, int(fake_msg_num), 0, 0, int(fake_msg_num)]), arbitration_id=MSGID_0, timestamp=0)


def test_msgid3():
    global fake_msg_num
    fake_msg_num = min(fake_msg_num + 0.1, 255)
    if fake_msg_num < 100:
        return None
    return Message(data=bytearray([int(fake_msg_num), 0, int(fake_msg_num), 0, 0, 0, int(fake_msg_num), 0]), arbitration_id=MSGID_3, timestamp=0)

def test_timer():
    global fake_msg_num
    fake_msg_num += 0.001
    if int(fake_msg_num) % 2 == 0:
        return None
    return Message(data=bytearray([]), arbitration_id=0, timestamp = 0)
