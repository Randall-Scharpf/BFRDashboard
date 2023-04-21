# This Python file uses the following encoding: utf-8
# written by Guo (Jason) Liu for Bruin Formula Racing
'''
resources.py is generated by Qt's resource system via this command: pyrcc5 resources.qrc -o resources.py
This command packages gui/resources and gui/main.ui into resources.py
for more reference website: https://www.pythonguis.com/tutorials/qresource-system/
'''

from receive import Receive
from datetime import datetime as dt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QFile, QTimer, QThreadPool, pyqtSignal, pyqtSlot
import resources, globalfonts, sys, datetime, traceback


# debugging constants, should be set to true in release
LOAD_UI_FROM_RES = True
FULL_SCREEN = True

# 1000 / interval = theoretical FPS cap
UPDATE_LOOP_INTERVAL = 10

# do throttle effect
THROTTLE_EFFECT = False

# time related
TIME_DISPLAY_FORMAT = '%m/%d/%y %I:%M:%S %p %a'
TIME_MONITOR_FORMAT = '%m/%d/%y %H:%M:%S'
TIME_LOG_FORMAT = '[%H:%M:%S]'

# how many seconds old a data would be considered obsolete
OBSOLETE_THRESHOLD = 1
# how many seconds ago the last update is can connection would be considered disconnected
DISCONNECTION_THRESHOLD = 1
# all the data we want to keep track of
DATA_KEYS = ['acc_x', 'acc_y', 'acc_z', 'acc_magnitude', 'battery', 'brake', 'coolant', 'engine_speed', 'exhaust', 'fan1', 'fuel_pressure', 'fuel_pump', 'gear', 'ignition_timing',
'injector_duty', 'intake', 'lambda1', 'lambda_target', 'log', 'lrt', 'map', 'mass_airflow', 'rotation_x',
'rotation_y', 'rotation_z', 'sd_status', 'switch', 'throttle', 'unk', 've', 'vehicle_speed']

# main data structure
data_dict = {}
for key in DATA_KEYS:
    data_dict[key] = {'value': None, 'prev_update_ts': -1, 'obs': -1, 'msg_count': 0, 'mps': -1}

'''
We use two clocks to keep track of time: system time and message timestamps. The system time of Raspberry Pi may very well be off
especially if it loses Internet access for a long period of time, but it is a continous clock. The message timestamps are accurate,
but they may not be continous. To calculate the precise moment of time, we get system time and apply a previously calculated offset to
convert it to message time. Every datetime object variable below are usually in system time, unless otherwise specified
'''
start_dt = dt.now()
# offset = message timestamp - system time
dt_offset = dt.now() - dt.now()
dt_offset_set = False
last_msg_dt = dt.now() - datetime.timedelta(seconds=1)
msg_count = 0

elapsed_errors = 0
elapsed_warnings = 0


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        # initialize data members
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
        self.dm_log("Loaded UI to main window")
        # scale widgets
        globalfonts.scale_size_for_all(self)
        # launch gui update loop
        qtimer = QTimer(self)
        qtimer.timeout.connect(self.update_gui)
        self.dm_log("Launching update loop, interval is " + str(UPDATE_LOOP_INTERVAL) +  "ms")
        qtimer.start(UPDATE_LOOP_INTERVAL)
        # launch receive
        self.dm_log("QThreadPool max thread count is " + str(QThreadPool.globalInstance().maxThreadCount()))
        pool = QThreadPool.globalInstance()
        self.receive_thread = Receive()
        self.receive_thread.signals.update_data.connect(self.update_data)
        self.receive_thread.signals.log_msg.connect(self.write_to_dm_msgtext)
        self.receive_thread.signals.error.connect(self.handle_error)
        self.dm_log("Launching receive thread")
        pool.start(self.receive_thread)
        # connecting signals
        self.ExitLabel.exit.connect(self.receive_thread.stop)
        self.ToggleDataMonitorLabel.on_toggle_data_monitor.connect(self.on_toggle_data_monitor)
        # show self
        if FULL_SCREEN:
            self.showFullScreen()
        else:
            self.show()
        self.dm_log("Current screen width: " + str(self.frameGeometry().width()) + "x" + str(self.frameGeometry().height()))

    # called by Receive thread
    @pyqtSlot(float, dict)
    def update_data(self, ts, dict):
        try:
            # adjust time offset
            global dt_offset, dt_offset_set
            dt_offset = dt.fromtimestamp(ts) - dt.now()
            dt_offset_set = True
            # record message
            global last_msg_dt, msg_count
            last_msg_dt = dt.now()
            msg_count += 1
            for key, value in dict.items():
                data_dict[key]['value'] = value
                data_dict[key]['prev_update_ts'] = ts
                data_dict[key]['msg_count'] += 1
        except Exception as e:
            self.handle_error(type(e).__name__,
            "Error at update_data() at ST " + str(dt.now()) + " or " + str(dt.now() + dt_offset),
            "timestamp=" + str(ts) + ", dict=" + str(dict),
            "Failed to update data",
            traceback.format_exc())

    def update_gui(self):
        try:
            # initialize time variables
            sys_dt_object = dt.now()
            adjusted_dt_object = dt_offset + sys_dt_object  # in message time
            self.log_time = adjusted_dt_object.strftime(TIME_LOG_FORMAT) if dt_offset_set else "ST" + adjusted_dt_object.strftime(TIME_LOG_FORMAT)
        except Exception as e:
            self.handle_error(type(e).__name__,
            "Error at update_gui() section 1 at ST " + str(dt.now()) + " or " + str(dt.now() + dt_offset),
            "",
            "Failed to retreieve time",
            traceback.format_exc())

        try:
            # gui update to dashboard based on latest message data
            if data_dict['battery']['prev_update_ts'] != -1:
                self.Battery.set_number(data_dict['battery']['value'])
                self.Battery.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['battery']['prev_update_ts'])).total_seconds() > OBSOLETE_THRESHOLD)
            if data_dict['coolant']['prev_update_ts'] != -1:
                self.CoolantTemp.set_number(data_dict['coolant']['value'])
                self.CoolantTemp.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['coolant']['prev_update_ts'])).total_seconds() > OBSOLETE_THRESHOLD)
            if data_dict['engine_speed']['prev_update_ts'] != -1:
                self.RPMDial.updateValue(data_dict['engine_speed']['value'])
                self.RPMDial.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['engine_speed']['prev_update_ts'])).total_seconds() > OBSOLETE_THRESHOLD)
            if data_dict['gear']['prev_update_ts'] != -1:
                if data_dict['gear']['value'] == 0:
                    self.Gear.gear.setText("N")
                else:
                    self.Gear.gear.setText(str(data_dict['gear']['value']))
                self.Gear.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['gear']['prev_update_ts'])).total_seconds() > OBSOLETE_THRESHOLD)
            if data_dict['fuel_pressure']['prev_update_ts'] != -1:
                self.Brake.set_number(data_dict['fuel_pressure']['value'])
                self.Brake.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['fuel_pressure']['prev_update_ts'])).total_seconds() > OBSOLETE_THRESHOLD)
            if data_dict['lambda1']['prev_update_ts'] != -1:
                self.LambdaDial.updateValue(data_dict['lambda1']['value'])
                self.LambdaDial.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['lambda1']['prev_update_ts'])).total_seconds() > OBSOLETE_THRESHOLD)
            if data_dict['vehicle_speed']['prev_update_ts'] != -1:
                self.SpeedDial.updateValue(data_dict['vehicle_speed']['value'])
                self.SpeedDial.set_obsolete((adjusted_dt_object - dt.fromtimestamp(data_dict['vehicle_speed']['prev_update_ts'])).total_seconds() > OBSOLETE_THRESHOLD)
            if data_dict['throttle']['prev_update_ts'] != -1:
                blur_ratio = min(1, max(0, data_dict['throttle']['value']))
                self.RPMRadialGradient.blur_ratio = blur_ratio
                self.LambdaRadialGradient.blur_ratio = blur_ratio
                self.SpeedRadialGradient.blur_ratio = blur_ratio
                if THROTTLE_EFFECT:
                    self.RPMRadialGradient.update()
                    self.LambdaRadialGradient.update()
                    self.SpeedRadialGradient.update()
            if data_dict['log']['prev_update_ts'] != -1:
                self.LogLabel.setText(data_dict['log']['value'])
        except Exception as e:
            self.handle_error(type(e).__name__,
            "Error at update_gui() section 2 at ST " + str(dt.now()) + " or " + str(dt.now() + dt_offset),
            "",
            "Failed to update data gui",
            traceback.format_exc())

        try:
            # give error box a chance to update itself
            elapsed_update_seconds = (sys_dt_object - self.prev_update_dt).total_seconds()
            self.ErrorBox.update_frame(elapsed_update_seconds)
            self.prev_update_dt = dt.now()
            # update cuurent time in message time on dashboard
            self.TimeLabel.setText(adjusted_dt_object.strftime(TIME_DISPLAY_FORMAT))
            # determine can connection based on time of last message received
            disconnection_time = int((sys_dt_object - last_msg_dt).total_seconds())
            if disconnection_time >= DISCONNECTION_THRESHOLD:
                self.CANConnectionLabel.setText('No Connection (' + str(min(99, disconnection_time)) + ')')
                self.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + 'color: red;' + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))
            else:
                self.CANConnectionLabel.setText('Connected')
                self.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + 'color: green;' + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))
            # determine if this update call is on a whole second (called once per second)
            elapsed_whole_update_seconds = (sys_dt_object - self.prev_whole_update_dt).total_seconds()
            is_whole_update = elapsed_whole_update_seconds > 1
            if is_whole_update:
                self.prev_whole_update_dt = 0
                self.prev_whole_update_dt = dt.now()
            # update FPS and MPS label
            if is_whole_update:
                global msg_count
                self.FPSLabel.setText("FPS: " + str(min(99, int(self.elapsed_updated_frames / elapsed_whole_update_seconds))) + "\nMPS: " + str(min(9999, int(msg_count / elapsed_whole_update_seconds))))
                self.elapsed_updated_frames = 0
                msg_count = 0
            self.elapsed_updated_frames += 1
            # check sd status
            if data_dict['sd_status']['prev_update_ts'] != -1 and data_dict['sd_status']['value'] == 0:
                self.handle_error('SD Status',
                "Error at update_gui() section 3 at ST " + str(dt.now()) + " or " + str(dt.now() + dt_offset),
                "sd_status=" + str(data_dict['sd_status']['value']),
                "SD Status not 0",
                traceback.format_exc())
            # check if switch is flipped
            if data_dict['switch']['value'] == 0:
                self.on_toggle_data_monitor(False)
                data_dict['switch']['value'] = None
        except Exception as e:
            self.handle_error(type(e).__name__,
            "Error at update_gui() section 3 at ST " + str(dt.now()) + " or " + str(dt.now() + dt_offset),
            "",
            "Failed to update misc gui",
            traceback.format_exc())

        try:
            # Data Monitor gui updates
            if self.DataMonitor.isVisible():
                # give two text edits a chance to update itself
                self.DataMonitor.MsgText.update_frame()
                self.DataMonitor.LogText.update_frame()
                # calculate obsoletion time and mps for each data
                for key in DATA_KEYS:
                    data_dict[key]['obs'] = (adjusted_dt_object - dt.fromtimestamp(data_dict[key]['prev_update_ts'])).total_seconds()
                    if is_whole_update:
                        data_dict[key]['mps'] = data_dict[key]['msg_count'] / elapsed_whole_update_seconds
                        data_dict[key]['msg_count'] = 0
                # update DataTables
                self.DataMonitor.DataTable1.update_frame(data_dict)
                self.DataMonitor.DataTable2.update_frame(data_dict)
                # update TimeTable
                if dt_offset_set:
                    time_table_dict = [(start_dt + dt_offset).strftime(TIME_MONITOR_FORMAT), adjusted_dt_object.strftime(TIME_MONITOR_FORMAT),
                    (last_msg_dt + dt_offset).strftime(TIME_MONITOR_FORMAT), str(dt_offset.total_seconds()), "E " + str(elapsed_errors) + " W " + str(elapsed_warnings)]
                    self.DataMonitor.TimeTable.update_values(time_table_dict)
                else:
                    time_table_dict = ["(ST) " + (start_dt).strftime(TIME_MONITOR_FORMAT), "(ST) " + sys_dt_object.strftime(TIME_MONITOR_FORMAT),
                    "(ST) " + last_msg_dt.strftime(TIME_MONITOR_FORMAT), str(dt_offset.total_seconds()), "E " + str(elapsed_errors) + " W " + str(elapsed_warnings)]
                    self.DataMonitor.TimeTable.update_values(time_table_dict)
        except Exception as e:
            self.handle_error(type(e).__name__,
            "Error at update_gui() section 4 at ST " + str(dt.now()) + " or " + str(dt.now() + dt_offset),
            "",
            "Failed to update data monitor",
            traceback.format_exc())

    # called by toggle data monitor button or by Receive thread
    @pyqtSlot(bool)
    def on_toggle_data_monitor(self, toggle_cursor):
        try:
            self.DataMonitor.setVisible(not self.DataMonitor.isVisible())
            if self.DataMonitor.isVisible() and toggle_cursor:
                self.setCursor(Qt.ArrowCursor)
            else:
                self.setCursor(Qt.BlankCursor)
        except Exception as e:
            self.handle_error(type(e).__name__,
            "Error at on_toggle_data_monitor() at ST " + str(dt.now()) + " or " + str(dt.now() + dt_offset),
            "toggle_cursor=" + str(toggle_cursor),
            "Failed to toggle data monitor",
            traceback.format_exc())


    # called by Receive thread to record a can message
    @pyqtSlot(str)
    def write_to_dm_msgtext(self, msg):
        try:
            self.DataMonitor.MsgText.push_back_line("<font color=\"gray\">" + self.log_time + "</font> " + msg)
        except Exception as e:
            print("Error at write_to_dm_msgtext() at ST " + str(dt.now()) + " or " + str(dt.now() + dt_offset))
            print("msg=" + str(msg))
            print(traceback.format_exc())

    # called by self and Receive thread to log an info message, warning or error
    @pyqtSlot(str)
    def dm_log(self, msg):
        try:
            self.DataMonitor.LogText.push_back_line("<font color=\"gray\">" + self.log_time + "</font> " + msg)
        except Exception as e:
            print("Error at dm_log() at ST " + str(dt.now()) + " or " + str(dt.now() + dt_offset))
            print("msg=" + str(msg))
            print(traceback.format_exc())

    @pyqtSlot(str, str, str, str, str)
    def handle_error(self, error_type, msg, param_msg, display_msg, traceback_str):
        try:
            self.DataMonitor.LogText.push_back_line("<font color=\"red\">[ERROR]</font> " +
            "<font color=\"gray\">" + self.log_time + "</font> " + msg + ". " + param_msg)
            self.DataMonitor.LogText.push_back_line(traceback_str.replace("\n", "<br>"))
            self.ErrorBox.error(error_type, display_msg)
            global elapsed_errors
            elapsed_errors += 1
        except Exception as e:
            print("Error at dm_log() at ST " + str(dt.now()) + " or " + str(dt.now() + dt_offset))
            print("msg=" + str(msg))
            print(traceback.format_exc())


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
