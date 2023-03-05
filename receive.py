from PyQt5.QtCore import QRunnable, Qt, QThreadPool, pyqtSignal
from can import Message
import os
import can
import timer


# os.system('sudo ip link set can0 type can bitrate 500000')
# os.system('sudo ifconfig can0 up')
# can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan') # socketcan_native

# https://www.aemelectronics.com/sites/default/files/aem_product_instructions/Infinity-ECU-Full-Manual.pdf
MSGID_1 = int("0x01F0A000", 0)


class Receive(QRunnable):
    def __init__(self, main_win):
        super().__init__()
        self.keep_running = True
        self.main_win = main_win
        self.i = 0

    def run(self):
        while self.keep_running: # networ
            # msg = can0.recv(10.0)
            self.i = self.i + 0.001
            if self.i > 255:
               self.i = 255
            msg = Message(data=bytearray([int(self.i),255,1]), arbitration_id=MSGID_1, is_extended_id = True)
            print(msg)
            if msg is None:
                print('Timeout occurred, no message.')
            else:
                self.parse_message(msg.arbitration_id, msg.data)
                timer.on_receive_data()

    def stop(self):
        self.keep_running = False
        os.system('sudo ifconfig can0 down')

    def parse_message(self, id, data):
        # RPM
        size = len(data)
        if id == MSGID_1:
            # check if size is good
            # byte 0-1, label Engine Speed, 16 bit unsigned, scaling 0.39063 rpm/bit, range 0 to 25,599.94 RPM
            rpm = (data[0] * 256 + data[1]) * 0.39063 / 1000
            self.main_win.RPMDial.updateValue(rpm)






