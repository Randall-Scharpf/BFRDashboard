from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF

WIDTH = 280
HEIGHT = 310


class GearWidget(QWidget):
    def __init__(self, parent=None):
        super(GearWidget, self).__init__(parent)

        label = QLabel(self)
        label.setText("GEAR")
        label.setStyleSheet("color: white; font-size : 50px; background-color : rgba(0, 0, 0, 0);")
        label.setGeometry(0, 40, WIDTH, 40)
        label.setAlignment(Qt.AlignCenter)

        self.gear = QLabel(self)
        self.gear.setText("N")
        self.gear.setStyleSheet("color: white; font-size : 250px; background-color : rgba(0, 0, 0, 0);")
        self.gear.setGeometry(0, 100, WIDTH, 200)
        self.gear.setAlignment(Qt.AlignCenter)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(182, 182, 182, 255), 5, Qt.SolidLine))
        painter.drawRoundedRect(QRectF(0, 0, WIDTH, HEIGHT), 40, 40)
