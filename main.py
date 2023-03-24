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

UPDATE_LOOP_INTERVAL = 10

USE_SYS_TIME = False
TIME_DISPLAY_FORMAT = '%m/%d/%y %I:%M:%S %p %a'
TIME_MONITOR_FORMAT = '%m/%d/%y %H:%M:%S'
TIME_LOG_FORMAT = '[%H:%M:%S]'
OBSOLETE_DATA_SEC = 1

DATA_KEYS = ['acc_x', 'acc_y', 'acc_z', 'acc_magnitude', 'battery', 'brake', 'coolant', 'engine_speed', 'exhaust', 'fan1', 'fuel_pressure', 'fuel_pump', 'gear', 'ignition_timing',
'injector_duty', 'intake', 'lambda1', 'lambda_target', 'log', 'lrt', 'map', 'mass_airflow', 'rotation_x',
'rotation_y', 'rotation_z', 'throttle', 'unk', 've', 'vehicle_speed']
data_dict = {}
for key in DATA_KEYS:
    data_dict[key] = {'value': None, 'prev_update_ts': -1, 'obs': -1, 'msg_count': 0, 'mps': -1}

start_dt = dt.now()
dt_offset = dt.now() - dt.now()
dt_offset_init = False
last_msg_dt = dt.now() - datetime.timedelta(seconds=1)
msg_count = 0

elapsed_errors = 0
elapsed_warnings = 0


@pyqtSlot(float, dict)
def update_data(ts, dict):
    global last_msg_dt, msg_count
    last_msg_dt = dt.now()
    msg_count += 1
    for key, value in dict.items():
        data_dict[key]['value'] = value
        data_dict[key]['prev_update_ts'] = ts
        data_dict[key]['msg_count'] += 1

@pyqtSlot(float)
def set_timestamp(timestamp):
    global dt_offset, dt_offset_init
    dt_offset = dt.fromtimestamp(timestamp) - dt.now()
    dt_offset_init = True


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        # initialize
        super(MainWindow, self).__init__()
        #
        self.elapsed_updated_frames = 0
        self.prev_whole_update_dt = dt.now()
        self.prev_update_dt = dt.now()
        self.log_time = dt.now().strftime("ST" + TIME_LOG_FORMAT)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # load UI
        if LOAD_UI_FROM_RES:
            main_ui = QFile(":/res/main_ui")
            main_ui.open(QFile.ReadOnly)
            uic.loadUi(main_ui, self)
        else:
            uic.loadUi("gui/main.ui", self)
        self.write_to_dmlogger(0, "Loaded UI to main window")
        # scale widgets
        globalfonts.scale_size_for_all(self)
        self.ToggleDataMonitorLabel.on_toggle_data_monitor.connect(self.on_toggle_data_monitor)
        # launch gui update loop
        qtimer = QTimer(self)
        qtimer.timeout.connect(self.update_gui)
        self.write_to_dmlogger(0, "Launching update loop, interval is " + str(UPDATE_LOOP_INTERVAL) +  "ms")
        qtimer.start(UPDATE_LOOP_INTERVAL)
        # launch receive
        self.write_to_dmlogger(0, "QThreadPool max thread count is " + str(QThreadPool.globalInstance().maxThreadCount()))
        pool = QThreadPool.globalInstance()
        self.receive_thread = Receive()
        self.receive_thread.signals.update_data.connect(update_data)
        self.receive_thread.signals.set_timestamp.connect(set_timestamp)
        self.receive_thread.signals.log_msg.connect(self.write_to_dm_msgtext)
        self.receive_thread.signals.log_text.connect(self.write_to_dmlogger)
        self.ExitLabel.exit.connect(self.receive_thread.stop)
        self.write_to_dmlogger(0, "Launching receive thread")
        pool.start(self.receive_thread)
        # show self
        if FULL_SCREEN:
            self.showFullScreen()
        else:
            self.show()
        self.write_to_dmlogger(0, "Current screen width: " + str(self.frameGeometry().width()) + "x" + str(self.frameGeometry().height()))
        self.i = 0

    def update_gui(self):
        sys_dt_object = dt.now()
        adjusted_dt_object = dt_offset + sys_dt_object
        self.log_time = adjusted_dt_object.strftime(TIME_LOG_FORMAT)

        if not dt_offset_init:
            self.log_time = "ST" + self.log_time
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
            self.LambdaDial.updateValue(data_dict['lambda1']['value'])
            self.LambdaDial.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['lambda1']['prev_update_ts'])).total_seconds() > OBSOLETE_DATA_SEC)
        if data_dict['vehicle_speed']['prev_update_ts'] != -1:
            self.SpeedDial.updateValue(data_dict['vehicle_speed']['value'])
            self.SpeedDial.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['vehicle_speed']['prev_update_ts'])).total_seconds() > OBSOLETE_DATA_SEC)
        if data_dict['throttle']['prev_update_ts'] != -1:
            blur_ratio = min(1, max(0, data_dict['throttle']['value'] / MAX_BLUR_THROTTLE))
            self.RPMRadialGradient.blur_ratio = blur_ratio
            self.LambdaRadialGradient.blur_ratio = blur_ratio
            self.SpeedRadialGradient.blur_ratio = blur_ratio
            self.RPMRadialGradient.update()
            self.LambdaRadialGradient.update()
            self.SpeedRadialGradient.update()

        self.TimeLabel.setText(adjusted_dt_object.strftime(TIME_DISPLAY_FORMAT))

        disconnection_time = int((sys_dt_object - last_msg_dt).total_seconds())
        if disconnection_time >= 1:
            self.CANConnectionLabel.setText('No Connection (' + str(min(99, disconnection_time)) + ')')
            self.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + 'color: red;' + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))
        else:
            self.CANConnectionLabel.setText('Connected')
            self.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + 'color: green;' + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))

        elapsed_whole_update_seconds = (sys_dt_object - self.prev_whole_update_dt).total_seconds()
        is_whole_update = elapsed_whole_update_seconds > 1
        if is_whole_update:
            self.prev_whole_update_dt = 0
            self.prev_whole_update_dt = dt.now()

        if is_whole_update:
            global msg_count
            self.FPSLabel.setText("FPS: " + str(min(99, int(self.elapsed_updated_frames / elapsed_whole_update_seconds))) + "\nMPS: " + str(min(9999, int(msg_count / elapsed_whole_update_seconds))))
            self.elapsed_updated_frames = 0
            msg_count = 0
        self.elapsed_updated_frames += 1

        elapsed_update_seconds = (sys_dt_object - self.prev_update_dt).total_seconds()
        self.ErrorBox.update_frame(elapsed_update_seconds)
        self.prev_update_dt = dt.now()

        if self.DataMonitor.isVisible():
            for key in DATA_KEYS:
                data_dict[key]['obs'] = (adjusted_dt_object - dt.fromtimestamp(data_dict[key]['prev_update_ts'])).total_seconds()
                if is_whole_update:
                    data_dict[key]['mps'] = data_dict[key]['msg_count'] / elapsed_whole_update_seconds
                    data_dict[key]['msg_count'] = 0
            self.DataMonitor.DataTable1.update_frame(data_dict)
            self.DataMonitor.DataTable2.update_frame(data_dict)
            # update TimeTable
            if dt_offset_init:
                time_table_dict = [(start_dt + dt_offset).strftime(TIME_MONITOR_FORMAT), adjusted_dt_object.strftime(TIME_MONITOR_FORMAT),
                (last_msg_dt + dt_offset).strftime(TIME_MONITOR_FORMAT), str(dt_offset.total_seconds()), "E " + str(elapsed_errors) + " W " + str(elapsed_warnings)]
                self.DataMonitor.TimeTable.update_values(time_table_dict)
            else:
                time_table_dict = ["(ST) " + (start_dt).strftime(TIME_MONITOR_FORMAT), "(ST) " + sys_dt_object.strftime(TIME_MONITOR_FORMAT),
                "(ST) " + last_msg_dt.strftime(TIME_MONITOR_FORMAT), str(dt_offset.total_seconds()), "E " + str(elapsed_errors) + " W " + str(elapsed_warnings)]
                self.DataMonitor.TimeTable.update_values(time_table_dict)
            self.DataMonitor.MsgText.update_frame()
            self.DataMonitor.LogText.update_frame()

    @pyqtSlot(bool)
    def on_toggle_data_monitor(self, toggle_cursor):
        self.DataMonitor.setVisible(not self.DataMonitor.isVisible())
        if self.DataMonitor.isVisible() and toggle_cursor:
            self.setCursor(Qt.ArrowCursor)
        else:
            self.setCursor(Qt.BlankCursor)

    @pyqtSlot(str)
    def write_to_dm_msgtext(self, msg):
        self.DataMonitor.MsgText.push_back_line("<font color=\"gray\">" + self.log_time + "</font> " + msg)

    @pyqtSlot(int, str)
    def write_to_dmlogger(self, type, msg):
        if type == 0:
            self.DataMonitor.LogText.push_back_line("<font color=\"gray\">" + self.log_time + "</font> " + msg)
        elif type == 1:
            self.DataMonitor.LogText.push_back_line("<font color=\"orange\">[WARNING]" + self.log_time + "</font> " + msg)
        else:
            self.DataMonitor.LogText.push_back_line( "<font color=\"red\">[ERROR]" + self.log_time + "</font> " + msg)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
