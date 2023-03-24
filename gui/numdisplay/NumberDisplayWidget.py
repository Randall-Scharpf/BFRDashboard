from PyQt5.QtWidgets import QWidget, QLabel
import globalfonts
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


WIDTH = 240
HEIGHT = 165
icon_size = 50

DIGIT_TO_FONTSIZE = {1 : 126, 2 : 106, 3 : 85, 4: 70}


class NumberDisplayWidget(QWidget):
    def __init__(self, icon_filepath, unit, flipped, allow_float=False, parent=None):
        super(NumberDisplayWidget, self).__init__(parent)
        self.allow_float = allow_float
        self.fontsize_css = globalfonts.scaled_css_size(126)
        self.color_css = globalfonts.WHITE_CSS

        pixmap = QPixmap(icon_filepath)
        pixmap = pixmap.scaledToWidth(icon_size)
        icon = QLabel(self)
        icon.setPixmap(pixmap)
        icon.setStyleSheet(globalfonts.TRANSPARENT_CSS)
        if flipped:
            icon.setGeometry(24, 84, icon_size, icon_size)
        else:
            icon.setGeometry(174, 84, icon_size, icon_size)

        self.numberLabel = QLabel(self)
        self.numberLabel.setText("N")
        if flipped:
            self.numberLabel.setGeometry(65, 0, 180, 168)
        else:
            self.numberLabel.setGeometry(6, 0, 180, 168)
        self.numberLabel.setAlignment(Qt.AlignCenter)
        self.__repaint_font()

        self.unitLabel = QLabel(self)
        self.unitLabel.setText(unit)
        self.unitLabel.setStyleSheet(globalfonts.FONT_CSS + globalfonts.WHITE_CSS + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(50))
        if flipped:
            self.unitLabel.setGeometry(24, 36, 48, 48)
        else:
            self.unitLabel.setGeometry(174, 36, 48, 48)
        self.unitLabel.setAlignment(Qt.AlignCenter)

    def set_number(self, num):
        if self.allow_float:
            num = round(num, 1)
        else:
            num = int(num)
        num_len = len(str(num))
        if (num_len < 1 or num_len > 4):
            self.fontsize_css = globalfonts.scaled_css_size(DIGIT_TO_FONTSIZE[4])
        else:
            self.fontsize_css = globalfonts.scaled_css_size(DIGIT_TO_FONTSIZE[num_len])
        self.numberLabel.setText(str(num))
        self.__repaint_font()

    def __repaint_font(self):
        self.numberLabel.setStyleSheet(globalfonts.FONT_CSS + globalfonts.TRANSPARENT_CSS + self.color_css + self.fontsize_css)

    def set_obsolete(self, obsolete):
        if obsolete:
            self.color_css = "color:rgba(170,170,170,255);"
        else:
            self.color_css = globalfonts.WHITE_CSS
        self.__repaint_font()


class BatteryDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(icon_filepath=":/res/battery", unit="V", flipped=True, allow_float=True, parent=parent)


class BrakeDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(icon_filepath=":/res/brake", unit="%", flipped=True, allow_float=False, parent=parent)


class CoolantDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(icon_filepath=":/res/coolant", unit="F", flipped=False, allow_float=False, parent=parent)


class ExhaustDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(icon_filepath=":/res/exhaust", unit="F", flipped=False, allow_float=False, parent=parent)
