from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPainter, QRadialGradient
from PyQt5.QtCore import Qt, QPoint


COLOR_MIN_RAD = 0.0
COLOR_SLOPE = 0.8
BLACK_MIN_RAD = 0.85
BLACK_SLOPE = 1


class RadialGradientEffect(QWidget):
    def __init__(self, parent=None):
        super(RadialGradientEffect, self).__init__(parent)
        self.blur_ratio = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        radialGradient = QRadialGradient(QPoint(self.width() / 2, self.height() / 2), self.width() / 2)
        radialGradient.setColorAt(COLOR_MIN_RAD + COLOR_SLOPE * self.blur_ratio, QColor(139, 225, 242, 255))
        radialGradient.setColorAt(min(1, BLACK_MIN_RAD + BLACK_SLOPE * self.blur_ratio), QColor(0, 0, 0, 0))
        painter.setBrush(radialGradient)
        painter.drawEllipse(0, 0, self.width(), self.height())
