from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF


class BorderBackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super(BorderBackgroundWidget, self).__init__(parent)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(116, 116, 116, 255), 5, Qt.SolidLine))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 40, 40)
        painter.drawLine(0, self.height() // 2, self.width(), self.height() // 2)
