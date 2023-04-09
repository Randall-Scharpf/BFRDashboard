from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QFile


# datas to display in the two data tables
DATA_TABLE1_KEYS = ['log', 'battery', 'brake', 'coolant', 'engine_speed', 'exhaust', 'gear', 'lambda1', 'throttle', 'vehicle_speed']
DATA_TABLE2_KEYS = ['acc_x', 'acc_y', 'acc_z', 'acc_magnitude', 'fan1', 'fuel_pressure', 'fuel_pump', 'ignition_timing', 'injector_duty',
'intake', 'lambda_target', 'lrt', 'map', 'mass_airflow', 'rotation_x', 'rotation_y', 'rotation_z', 'sd_status', 've', 'unk']
TIME_TABLE_TITLES = ["Start time", "Current time", "Last message", "DT offset", "Elapsed erros & warnings"]


class DataMonitor(QWidget):
    def __init__(self, parent=None):
        super(DataMonitor, self).__init__(parent)
        # invisible by default
        self.hide()
        # load UI
        main_ui = QFile(":/res/data_monitor_ui")
        main_ui.open(QFile.ReadOnly)
        uic.loadUi(main_ui, self)
        # initialize widgets
        self.DataTable1.init(DATA_TABLE1_KEYS)
        self.DataTable2.init(DATA_TABLE2_KEYS)
        self.TimeTable.init(TIME_TABLE_TITLES)
        self.MsgText.init(50, True, fixed_height=400)
        self.LogText.init(100, True)
