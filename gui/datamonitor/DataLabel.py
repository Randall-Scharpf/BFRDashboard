from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
import globalfonts as gf


# a helper label
class DataLabel(QLabel):
    def __init__(self, text="", font_size=20, align_center=False, fixed_width=None, word_wrap=False, parent=None):
        super(DataLabel, self).__init__(parent)
        self.setStyleSheet(gf.WHITE_CSS + gf.TRANSPARENT_CSS + gf.FONT_CSS + gf.scaled_css_size(font_size))
        if align_center:
            self.setAlignment(Qt.AlignCenter)
        self.setText(text)
        if fixed_width is not None:
            self.setFixedWidth(fixed_width)
        self.setWordWrap(word_wrap)

    def set_number(self, num, round_dec_place=2):
        if isinstance(num, str):
            self.setText(num)
        else:
            self.setText(str(round(num, round_dec_place)))
