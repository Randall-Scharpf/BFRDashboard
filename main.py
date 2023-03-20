# This Python file uses the following encoding: utf-8
# written by Guo (Jason) Liu for Bruin Formula Racing
'''
resources.py is generated by Qt's resource system via this command: pyrcc5 resources.qrc -o resources.py
This command packages gui/resources and gui/main.ui into resources.py
for more reference website: https://www.pythonguis.com/tutorials/qresource-system/
'''
import resources, globalfonts
import sys
from receive import Receive
import datetime
from datetime import datetime as dt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QFile, QTimer, QThreadPool, QCoreApplication, pyqtSignal, pyqtSlot


LOAD_UI_FROM_RES = False
FULL_SCREEN = False
MAX_BLUR_THROTTLE = 50

USE_SYS_TIME = False
TIME_DISPLAY_FORMAT = '%m/%d/%y %I:%M:%S %p %a'
OBSOLETE_DATA_SEC = 1

DATA_KEYS = ['battery', 'coolant', 'engine_speed', 'exhaust', 'fan1', 'fuel_pressure', 'fuel_pump', 'gear', 'ignition_timing',
'injector_duty', 'intake', 'lambda1', 'lambda_target', 'lrt', 'map', 'mass_airflow', 'rotation_x',
'rotation_y', 'rotation_z', 'throttle', 've', 'vehicle_speed'] # acceleration
data_dict = {}
for key in DATA_KEYS:
    data_dict[key] = {'value': None, 'prev_update_ts': -1}
dt_offset = dt.now() - dt.now()
last_msg_dt = dt.now() - datetime.timedelta(seconds=1)
msg_count = 0

@pyqtSlot(float, dict)
def update_data(ts, dict):
    global last_msg_dt, msg_count
    last_msg_dt = dt.now()
    msg_count += 1
    for key, value in dict.items():
        data_dict[key]['value'] = value
        data_dict[key]['prev_update_ts'] = ts

@pyqtSlot(float)
def init_timestamp(timestamp):
    global dt_offset
    dt_offset = dt.fromtimestamp(timestamp) - dt.now()


class MainWindow(QMainWindow):
    __elapsed_updated_frames = 0
    __prev_whole_update_dt = dt.now()
    __prev_update_dt = dt.now()

    def __init__(self, parent=None):
        # initialize
        QMainWindow.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # load UI
        if LOAD_UI_FROM_RES:
            main_ui = QFile(":/res/main_ui")
            main_ui.open(QFile.ReadOnly)
            uic.loadUi(main_ui, self)
        else:
            uic.loadUi("gui/main.ui", self)

        # scale widgets
        globalfonts.scale_size_for_all(self)

        # launch gui update loop
        qtimer = QTimer(self)
        qtimer.timeout.connect(self.update_gui)
        qtimer.start(10)

        # launch receive
        print('QThreadPool max thread count is ' + str(QThreadPool.globalInstance().maxThreadCount()))
        pool = QThreadPool.globalInstance()

        self.receive_thread = Receive()
        self.receive_thread.signals.update_data.connect(update_data)
        self.receive_thread.signals.init_timestamp.connect(init_timestamp)
        self.ExitLabel.exit.connect(self.receive_thread.stop)
        pool.start(self.receive_thread)

        # show self
        if FULL_SCREEN:
            self.showFullScreen()
        else:
            self.show()
        print("Current screen width: " + str(self.frameGeometry().width()) + ", height: " + str(self.frameGeometry().height()))
        self.setCursor(Qt.BlankCursor)

    def update_gui(self):
        sys_dt_object = dt.now()
        adjusted_dt_object = dt_offset + sys_dt_object

        if data_dict['battery']['prev_update_ts'] != -1:
            self.Battery.set_number(data_dict['battery']['value'])
            self.Battery.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['battery']['prev_update_ts'])).total_seconds() > OBSOLETE_DATA_SEC)
        if data_dict['coolant']['prev_update_ts'] != -1:
            self.CoolantTemp.set_number(data_dict['coolant']['value'])
            self.CoolantTemp.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['coolant']['prev_update_ts'])).total_seconds() > OBSOLETE_DATA_SEC)
        if data_dict['engine_speed']['prev_update_ts'] != -1:
            self.RPMDial.updateValue(data_dict['engine_speed']['value'])
            self.RPMDial.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['engine_speed']['prev_update_ts'])).total_seconds() > OBSOLETE_DATA_SEC)
        if data_dict['gear']['prev_update_ts'] != -1:
            self.Gear.gear.setText(str(data_dict['gear']['value']))
            self.Gear.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['gear']['prev_update_ts'])).total_seconds() > OBSOLETE_DATA_SEC)
        if data_dict['lambda1']['prev_update_ts'] != -1:
            self.AFRDial.updateValue(data_dict['lambda1']['value'])
            self.AFRDial.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['lambda1']['prev_update_ts'])).total_seconds() > OBSOLETE_DATA_SEC)
        if data_dict['vehicle_speed']['prev_update_ts'] != -1:
            self.VelocityDial.updateValue(data_dict['vehicle_speed']['value']) # TODO change velocity to speed
            self.VelocityDial.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['vehicle_speed']['prev_update_ts'])).total_seconds() > OBSOLETE_DATA_SEC)
        if data_dict['throttle']['prev_update_ts'] != -1:
            blur_ratio = min(1, max(0, data_dict['throttle']['value'] / MAX_BLUR_THROTTLE))
            self.RPMDial.set_blur_effect(blur_ratio)
            self.AFRDial.set_blur_effect(blur_ratio)
            self.VelocityDial.set_blur_effect(blur_ratio)

        self.TimeLabel.setText(adjusted_dt_object.strftime(TIME_DISPLAY_FORMAT))

        disconnection_time = int((sys_dt_object - last_msg_dt).total_seconds())
        if disconnection_time >= 1:
            self.CANConnectionLabel.setText('No Connection (' + str(min(99, disconnection_time)) + ')')
            self.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + 'color: red;' + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))
        else:
            self.CANConnectionLabel.setText('Connected')
            self.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + 'color: green;' + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))

        elapsed_fps_update_seconds = (sys_dt_object - self.__prev_whole_update_dt).total_seconds()
        if elapsed_fps_update_seconds > 1:
            global msg_count
            self.FPSLabel.setText("FPS: " + str(min(99, int(self.__elapsed_updated_frames / elapsed_fps_update_seconds))) + "\nMPS: " + str(min(9999, int(msg_count / elapsed_fps_update_seconds))))
            self.__elapsed_updated_frames = 0
            self.__prev_whole_update_dt = dt.now()
            msg_count = 0
        self.__elapsed_updated_frames += 1

        elapsed_update_seconds = (sys_dt_object - self.__prev_update_dt).total_seconds()
        self.ErrorBox.update_frame(elapsed_update_seconds)
        self.__prev_update_dt = dt.now()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
