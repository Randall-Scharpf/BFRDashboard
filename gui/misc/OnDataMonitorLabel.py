from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal


class OnDataMonitorLabel(QLabel):
    on_data_monitor_turned_on = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, ev):
        self.on_data_monitor_turned_on.emit()
