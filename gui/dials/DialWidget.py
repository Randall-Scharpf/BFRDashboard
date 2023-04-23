from gui.dials.AnalogGaugeWidget import AnalogGaugeWidget
from PyQt5.QtGui import QColor
import globalfonts


class Dial(AnalogGaugeWidget):
    def __init__(self, parent, value_float, scale_float, shine_color, min_value, max_value, scala_count, angle_start, angle_size, scale_fontsize, value_fontsize):
        super(Dial, self).__init__(parent, value_float, scale_float)
        self.setCustomGaugeTheme(color1='#242321', color2=shine_color, color3='#000000')
        self.NeedleColor = QColor(139, 225, 242, 255)
        self.ScaleValueColor = QColor(139, 225, 242, 255)
        self.bigScaleMarker = QColor(139, 225, 242, 255)
        self.fineScaleColor = QColor(139, 225, 242, 255)
        self.DisplayValueColor = QColor(206, 244, 255, 255)
        self.value = min_value
        self.minValue = min_value
        self.maxValue = max_value
        self.scalaCount = scala_count
        self.scale_angle_start_value = angle_start
        self.scale_angle_size = angle_size
        self.scale_fontsize = globalfonts.scaled_dial_size(scale_fontsize)
        self.value_fontsize = globalfonts.scaled_dial_size(value_fontsize)
        self.obsolete = False

    def set_obsolete(self, obsolete):
        if obsolete:
            self.DisplayValueColor = QColor(170, 170, 170, 255)
        else:
            self.DisplayValueColor = QColor(206, 244, 255, 255)
        if obsolete ^ self.obsolete:
            self.update()
            self.obsolete = obsolete


class RPMDial(Dial):
    def __init__(self, parent=None):
        super(RPMDial, self).__init__(parent, value_float=True, scale_float=False, shine_color='#969696', min_value=0, max_value=14,
        scala_count=7, angle_start=155, angle_size=230, scale_fontsize=43, value_fontsize=75)


class SpeedDial(Dial):
    def __init__(self, parent=None):
        super(SpeedDial, self).__init__(parent, value_float=False, scale_float=False, shine_color='#757575', min_value=0, max_value=80,
        scala_count=8, angle_start=145, angle_size=150, scale_fontsize=23, value_fontsize=46)


class LambdaDial(Dial):
    def __init__(self, parent=None):
        super(LambdaDial, self).__init__(parent, value_float=True, scale_float=True, shine_color='#5e5e5e', min_value=0.5, max_value=1.5,
        scala_count=2, angle_start=255, angle_size=130, scale_fontsize=26, value_fontsize=51)
