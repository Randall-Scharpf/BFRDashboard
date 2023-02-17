from PyQt5.QtWidgets import QLabel


class ExitLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, ev):
        exit()
