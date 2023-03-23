from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal


class ToggleDataMonitorLabel(QLabel):
    on_toggle_data_monitor = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, ev):
        self.on_toggle_data_monitor.emit(True)
