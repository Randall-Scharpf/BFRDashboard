from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import globalfonts as gf


ICON_SIZE = 50
DIGIT_TO_FONTSIZE = {1 : 126, 2 : 106, 3 : 85, 4: 70}


class NumberDisplayWidget(QWidget):
    def __init__(self, icon_filepath, unit, flipped, allow_float=False, parent=None):
        super(NumberDisplayWidget, self).__init__(parent)
        # if number is a float or an int
        self.allow_float = allow_float
        # keeps track of fontsize and color
        self.fontsize_css = gf.scaled_css_size(126)
        self.color_css = gf.WHITE_CSS
        # load icon
        pixmap = QPixmap(icon_filepath)
        pixmap = pixmap.scaledToWidth(ICON_SIZE)
        icon = QLabel(self)
        icon.setPixmap(pixmap)
        icon.setStyleSheet(gf.TRANSPARENT_CSS)
        if flipped:
            icon.setGeometry(24, 84, ICON_SIZE, ICON_SIZE)
        else:
            icon.setGeometry(174, 84, ICON_SIZE, ICON_SIZE)
        # load number label
        self.numberLabel = QLabel(self)
        self.numberLabel.setText("N")
        if flipped:
            self.numberLabel.setGeometry(65, 0, 180, 168)
        else:
            self.numberLabel.setGeometry(6, 0, 180, 168)
        self.numberLabel.setAlignment(Qt.AlignCenter)
        self.repaint_font()
        # load unit label
        self.unitLabel = QLabel(self)
        self.unitLabel.setText(unit)
        unit_size = 50
        unit_width = 48
        if len(unit) == 4:
            unit_size = 30
            unit_width = 68
        self.unitLabel.setStyleSheet(gf.FONT_CSS + gf.WHITE_CSS + gf.TRANSPARENT_CSS + gf.scaled_css_size(unit_size))
        if flipped:
            self.unitLabel.setGeometry(24, 36, unit_width, 48)
        else:
            self.unitLabel.setGeometry(174, 36, unit_width, 48)
        self.unitLabel.setAlignment(Qt.AlignCenter)

        self.obsolete = False

    # called by main update loop to change number label's text
    def set_number(self, num):
        if self.allow_float:
            num = round(num, 1)
        else:
            num = int(num)
        num_len = len(str(num))
        if (num_len < 1 or num_len > 4):
            self.fontsize_css = gf.scaled_css_size(DIGIT_TO_FONTSIZE[4])
        else:
            self.fontsize_css = gf.scaled_css_size(DIGIT_TO_FONTSIZE[num_len])
        self.numberLabel.setText(str(num))
        self.repaint_font()

    # helper function, resets self's style sheet
    def repaint_font(self):
        self.numberLabel.setStyleSheet(gf.FONT_CSS + gf.TRANSPARENT_CSS + self.color_css + self.fontsize_css)

    def set_obsolete(self, obsolete):
        if obsolete:
            self.color_css = "color:rgba(170,170,170,255);"
        else:
            self.color_css = gf.WHITE_CSS
        if obsolete ^ self.obsolete:
            self.repaint_font()
            self.obsolete = obsolete


class BatteryDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(icon_filepath=":/res/battery", unit="V", flipped=True, allow_float=True, parent=parent)


class BrakeDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(icon_filepath=":/res/fuel_pressure", unit="PSIg", flipped=True, allow_float=False, parent=parent)


class CoolantDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(icon_filepath=":/res/coolant", unit="F", flipped=False, allow_float=False, parent=parent)


class ExhaustDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(icon_filepath=":/res/exhaust", unit="F", flipped=False, allow_float=False, parent=parent)
