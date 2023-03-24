from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent
import globalfonts as gf


FONT_SIZE = 16

class LenCapText(QTextEdit):
    def __init__(self, parent=None):
        super(QTextEdit, self).__init__(parent)
        self.setStyleSheet(gf.WHITE_CSS + gf.TRANSPARENT_CSS + gf.FONT_CSS + gf.scaled_css_size(FONT_SIZE) + "border:1px solid white;")
        self.setReadOnly(True)
        self.lines_queue = []
        self.max_len = 0
        # not freezable: -1, not freezed: 0, freezed: 1
        self.freeze_state = -1
        self.len = 0

    def init(self, max_len, freezable, fixed_height=None):
        self.max_len = max_len
        if freezable:
            self.freeze_state = 0
        else:
            self.freeze_state = -1
        if fixed_height is not None:
            self.setFixedHeight(fixed_height)

    def push_back_line(self, line):
        self.lines_queue.append(line)
        self.len += 1
        if self.len > self.max_len:
            self.lines_queue.pop(0)

    def update_frame(self):
        if self.freeze_state != 1:
            self.setText('<br>'.join(self.lines_queue))
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def mouseDoubleClickEvent(self, event):
        if self.freeze_state != -1:
            if self.freeze_state == 0:
                self.freeze_state = 1
            elif self.freeze_state == 1:
                self.freeze_state = 0


