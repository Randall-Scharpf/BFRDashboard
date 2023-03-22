from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent
import globalfonts as gf


FONT_SIZE = 16

class LenCapText(QTextEdit):
    def __init__(self, parent=None):
        super(QTextEdit, self).__init__(parent)
        self.setStyleSheet(gf.WHITE_CSS + gf.TRANSPARENT_CSS + gf.FONT_CSS + gf.scaled_css_size(FONT_SIZE) + "border:1px solid white;")
        self.setReadOnly(True)
        self.__lines_queue = []
        self.__max_len = 0
        # not freezable: -1, not freezed: 0, freezed: 1
        self.__freeze_state = -1
        self.__len = 0

    def init(self, max_len, freezable, fixed_height=None):
        self.__max_len = max_len
        if freezable:
            self.__freeze_state = 0
        else:
            self.__freeze_state = -1
        if fixed_height is not None:
            self.setFixedHeight(fixed_height)

    def push_back_line(self, line):
        self.__lines_queue.append(line)
        self.__len += 1
        if self.__len > self.__max_len:
            self.__lines_queue.pop(0)

    def update_frame(self):
        if self.__freeze_state != 1:
            self.setText('<br>'.join(self.__lines_queue))
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def mouseDoubleClickEvent(self, event):
        if self.__freeze_state != -1:
            if self.__freeze_state == 0:
                self.__freeze_state = 1
            elif self.__freeze_state == 1:
                self.__freeze_state = 0


