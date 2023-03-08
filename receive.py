from PyQt5.QtCore import QRunnable, Qt, QThreadPool, pyqtSignal
from can import Message
import os
import can
import time


PROCESS_FAKE_MSG = True
fake_msg_num = 0

if not PROCESS_FAKE_MSG:
    os.system('sudo ip link set can0 type can bitrate 500000')
    os.system('sudo ifconfig can0 up')
    can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

# https://www.aemelectronics.com/sites/default/files/aem_product_instructions/Infinity-ECU-Full-Manual.pdf
# https://www.pragmaticlinux.com/2021/10/can-communication-on-the-raspberry-pi-with-socketcan/
# https://www.waveshare.com/w/upload/2/29/RS485-CAN-HAT-user-manuakl-en.pdf
# https://forums.raspberrypi.com/viewtopic.php?t=141052
# https://harrisonsand.com/posts/can-on-the-raspberry-pi/

MSGID_1 = int("0x01F0A000", 0)
MSGID_2 = int("0x01F0A003", 0)


class Receive(QRunnable):
    def __init__(self, main_win):
        super().__init__()
        self.keep_running = True
        self.main_win = main_win

    def run(self):
        while self.keep_running: # networ
            if PROCESS_FAKE_MSG:
                time.sleep(0.01)
                msg = test_msgid1()
            else:
                msg = can0.recv(10.0)
            print(msg)
            if msg is None:
                print('Timeout occurred, no message.')
            else:
                self.parse_message(msg.arbitration_id, msg.data)

    def stop(self):
        self.keep_running = False
        if not PROCESS_FAKE_MSG:
            os.system('sudo ifconfig can0 down')

    def parse_message(self, id, data):
        size = len(data)
        if id == MSGID_1:
            # TOOD: check if size is good
            # byte 0-1, Engine Speed, 16 bit unsigned, scaling 0.39063 rpm/bit, range 0 to 25,599.94 RPM
            rpm = (data[0] * 256 + data[1]) * 0.39063 / 1000
            self.main_win.RPMDial.updateValue(rpm)

            # byte 4-5, Throttle, 16 bit unsigned, scaling 0.0015259 %/bit, range 0 to 99.998 %
            throttle = (data[4] * 256 + data[5]) * 0.0015259
            blur_ratio = min(1, max(0, 2 * throttle / 100))  # TODO: what is considered a large throttle?
            self.main_win.RPMDial.set_blur_effect(blur_ratio)
            self.main_win.AFRDial.set_blur_effect(blur_ratio)
            self.main_win.VelocityDial.set_blur_effect(blur_ratio)  # TODO: which one looks better?

            # byte 7, Coolant Temp,  8 bit signed 2's comp, scaling 1 Deg C/bit 0, range -128 to 127 C
            coolant = data[7] - 128
            self.main_win.CoolantTemp.set_number(coolant)

            print("rpm", rpm, "throttle", throttle, "coolant", coolant)
        elif id == MSGID_2:
            # byte 0, Lambda #1, 8 bit unsigned, scaling 0.00390625 Lambda/bit, offset 0.5, range 0.5 to 1.496 Lambda
            lambda1 = data[0] * 0.00390625 + 0.5  # TODO: Lambda 1 or lambda 2 or lambda target?
            # self.main_win.AFRDial.updateValue(lambda1)

            # byte 2-3, Vehicle Speed, 16 bit unsigned, scaling 0.0062865 kph/bit, range 0 to 411.986 km/h
            speed = (data[2] * 256 + data[3]) * 0.0062865
            # self.main_win.VelocityDial.updateValue(speed)

            # 6-7 Battery Volts 16 bit unsigned 0.0002455 V/bit 0 to 16.089 Volts
            battery = (data[6] * 256 + data[7]) * 0.0002455
            self.main_win.Battery.set_number(battery)

            print("lambda1", lambda1, "speed", speed, "battery", battery)
        # TODO: where is brake?

        self.main_win.update_timer.on_receive_data()


def test_msgid1():
    global fake_msg_num
    fake_msg_num = min(fake_msg_num + 0.1, 255)
    return Message(data=bytearray([int(fake_msg_num), 0, 0, 0, int(fake_msg_num), 0, 0, int(fake_msg_num)]), arbitration_id=MSGID_1)


def test_msgid2():
    global fake_msg_num
    fake_msg_num = min(fake_msg_num + 0.1, 255)
    return Message(data=bytearray([int(fake_msg_num), 0, int(fake_msg_num), 0, 0, 0, int(fake_msg_num), 0]), arbitration_id=MSGID_2)
