from PyQt5.QtWidgets import QWidget, QLabel
import globalfonts
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


# widget's width = 140, height = 150
WIDTH = 180
HEIGHT = 165
icon_size = 50


class NumberDisplayWidget(QWidget):
    def __init__(self, icon_filepath, unit, flipped, parent=None):
        super(NumberDisplayWidget, self).__init__(parent)

        pixmap = QPixmap(icon_filepath)
        pixmap = pixmap.scaledToWidth(icon_size)
        icon = QLabel(self)
        icon.setPixmap(pixmap)
        icon.setStyleSheet("background-color : rgba(0, 0, 0, 0);")
        if flipped:
            icon.setGeometry(24, 84, icon_size, icon_size)
        else:
            icon.setGeometry(114, 84, icon_size, icon_size)

        self.numberLabel = QLabel(self)
        self.numberLabel.setText("N")
        self.numberLabel.setStyleSheet("color: white; background-color : rgba(0, 0, 0, 0);" + globalfonts.scaled_css_size(96))
        if flipped:
            self.numberLabel.setGeometry(60, 12, 120, 168)
        else:
            self.numberLabel.setGeometry(6, 12, 120, 168)
        self.numberLabel.setAlignment(Qt.AlignCenter)

        self.unitLabel = QLabel(self)
        self.unitLabel.setText(unit)
        self.unitLabel.setStyleSheet("color: white; background-color : rgba(0, 0, 0, 0);" + globalfonts.scaled_css_size(50))
        if flipped:
            self.unitLabel.setGeometry(24, 36, 48, 48)
        else:
            self.unitLabel.setGeometry(114, 36, 48, 48)
        self.unitLabel.setAlignment(Qt.AlignCenter)

    def _setNumberColor(self, r, g, b):
        color_str = "rgba(" + str(r) + "," + str(g) + "," + str(b) + ",255)"
        self.unitLabel.setStyleSheet("color: " + color_str + "; background-color : rgba(0, 0, 0, 0);" + globalfonts.scaled_css_size(50))
        self.numberLabel.setStyleSheet("color: " + color_str + "; background-color : rgba(0, 0, 0, 0);" +  + globalfonts.scaled_css_size(96))
