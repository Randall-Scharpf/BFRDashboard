from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
from can import Message
import os, can, time, traceback


# for debugging only, set to false on release
PROCESS_FAKE_MSG = True
fake_msg_num = 0

# open up can0 channel, reference RS485 manual: https://www.waveshare.com/w/upload/2/29/RS485-CAN-HAT-user-manuakl-en.pdf
if not PROCESS_FAKE_MSG:
    os.system('sudo ip link set can0 type can bitrate 500000')
    os.system('sudo ifconfig can0 up')
    can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

# reference Infinity ECU manual for processing data
# https://www.aemelectronics.com/sites/default/files/aem_product_instructions/Infinity-ECU-Full-Manual.pdf
TIMEOUT = 10
MSGID_0 = 0x01F0A000
MSGID_3 = 0x01F0A003
MSGID_4 = 0x01F0A004
MSGID_5 = 0x01F0A005
MSGID_6 = 0x00DA5400
MSGID_7 = 0x00DA5401
MSGID_8 = 0x00DA5402
MSGID_9 = 0x01F0A002


def unsigned_int_to_signed8(i):
    return i if i < 128 else i - 256


# celcius to fahrenheit, duh Americans
def c_to_f(c):
    return c * 1.8 + 32


class Receive(QRunnable):
    # the "better" way to do this is to make Receive a QObject that owns a QRunnable
    # as you can only declare signals in a QObject but not a QRunnable
    class SignalHelper(QObject):
        update_data = pyqtSignal(float, dict)
        log_msg = pyqtSignal(str)
        error = pyqtSignal(str, str, str, str, str)
    signals = SignalHelper()

    def __init__(self):
        super(Receive, self).__init__()
        self.keep_running = True

    # Receive loop
    def run(self):
        while self.keep_running:
            try:
                if PROCESS_FAKE_MSG:
                    time.sleep(0.001)
                    msg = test_msgid0()
                else:
                    msg = can0.recv(TIMEOUT)
                if msg is not None:
                    self.parse_message(msg.arbitration_id, msg.timestamp, msg.data)
                    self.signals.log_msg.emit(str(msg))
            except Exception as e:
                if not self.keep_running:
                    return
                self.signals.error.emit(type(e).__name__,
                "Error at run()",
                "",
                "Failed to retrieve message",
                traceback.format_exc())


    # called by ExitLabel's exit signal
    def stop(self):
        self.keep_running = False
        if not PROCESS_FAKE_MSG:
            os.system('sudo ifconfig can0 down')

    # process a can message
    def parse_message(self, id, timestamp, data):
        try:
            data_dict = {}
            if id == MSGID_0:
                # byte 0-1, Engine Speed, 16 bit unsigned, scaling 0.39063 rpm/bit, range 0 to 25,599.94 RPM
                data_dict['engine_speed'] = (data[0] * 256 + data[1]) * 0.39063 / 1000
                # byte 4-5, Throttle, 16 bit unsigned, scaling 0.0015259 %/bit, range 0 to 99.998 %
                data_dict['throttle'] = (data[4] * 256 + data[5]) * 0.0015259 / 100
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
            elif id == MSGID_6:
                # Bytes 0-3: first four characters of log name, as ASCII, Byte 4: SD status, 0 if all is well
                data_dict['log'] = chr(data[0]) + chr(data[1]) + chr(data[2]) + chr(data[3])
                data_dict['sd_status'] = data[4]
            elif id == MSGID_7:
                # Bytes 0-1: Exhaust gas temperature, signed, MSB first, scaling 0.0625
                data_dict['exhaust'] = (data[0] * 256 + data[1]) * 0.0625
            elif id == MSGID_8:
                # Byte 0: Index of which button was pressed. 0 for GUI switch button, 1 for other button
                data_dict['switch'] = data[0]
            elif id == MSGID_9:
                # Byte 0-1: Label ADCR18, 16 bit unsigned, scaling 0.00007782 range 0 to 5.0999 V
                data_dict['brake'] = (data[0] * 256 + data[1]) * 0.00007782 / 5.0999 * 100
            else:
                data_dict['unk'] = 0
            self.signals.update_data.emit(timestamp, data_dict)
        except Exception as e:
            self.signals.error.emit(type(e).__name__,
            "Error at parse_message()",
            "id=" + str(id) + ", timestamp=" + str(timestamp) + ", data=" + str(data),
            "Failed to parse message",
            traceback.format_exc())


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
