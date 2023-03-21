from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QFile


LOAD_UI_FROM_RES = False
DATA_TABLE1_KEYS = ['log', 'battery', 'brake', 'coolant', 'engine_speed', 'exhaust', 'gear', 'lambda1', 'throttle', 'vehicle_speed']
DATA_TABLE2_KEYS = []


class DataMonitor(QWidget):
    def __init__(self, parent=None):
        super(DataMonitor, self).__init__(parent)
        self.hide()
        if LOAD_UI_FROM_RES:
            main_ui = QFile(":/res/data_monitor_ui")
            main_ui.open(QFile.ReadOnly)
            uic.loadUi(main_ui, self)
        else:
            uic.loadUi("gui/datamonitor/data_monitor.ui", self)
        self.DataTable1.init(DATA_TABLE1_KEYS)

    def update_frame(self, data_dict):
        self.DataTable1.update_frame(data_dict)
