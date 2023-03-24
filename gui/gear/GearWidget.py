from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF
import globalfonts as gf


WIDTH = 280


class GearWidget(QWidget):
    def __init__(self, parent=None):
        super(GearWidget, self).__init__(parent)

        label = QLabel(self)
        label.setText("GEAR")
        label.setStyleSheet(gf.FONT_CSS + gf.WHITE_CSS + gf.TRANSPARENT_CSS + gf.scaled_css_size(50))
        label.setGeometry(0, 40, WIDTH, 40)
        label.setAlignment(Qt.AlignCenter)

        self.gear = QLabel(self)
        self.gear.setText("N")
        self.gear.setStyleSheet(gf.FONT_CSS + gf.WHITE_CSS + gf.TRANSPARENT_CSS + gf.scaled_css_size(250))
        self.gear.setGeometry(0, 85, WIDTH, 200)
        self.gear.setAlignment(Qt.AlignCenter)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(182, 182, 182, 255), 5, Qt.SolidLine))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 40, 40)

    def set_obsolete(self, obsolete):
        if obsolete:
            self.gear.setStyleSheet(gf.FONT_CSS + gf.OBSOLETE_COLOR_CSS + gf.TRANSPARENT_CSS + gf.scaled_css_size(250))
        else:
            self.gear.setStyleSheet(gf.FONT_CSS + gf.WHITE_CSS + gf.TRANSPARENT_CSS + gf.scaled_css_size(250))
