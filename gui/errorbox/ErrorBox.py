from PyQt5.QtWidgets import QLabel


SHOW_X = 1100
HIDE_X = 1260
MOVE_PX_PER_SEC = 200
STAY_TIME = 5
HEIGHT_PAD = 10


class ErrorBox(QLabel):
    def __init__(self, parent=None):
        super(ErrorBox, self).__init__(parent)
        # 0: hide and do nothing, 1: slide into the screen, 2: stay for a period of time, 3: slide back
        self.state = 0
        self.elapsed_stay_sec = 0
        self.float_x = HIDE_X
        self.setFixedWidth(160)
        self.hide()

    def update_frame(self, elapsed_sec):
        if self.state == 0:
            return
        elif self.state == 1:
            if self.float_x <= SHOW_X:
                self.state = 2
                self.elapsed_stay_sec = 0
            else:
                self.float_x -= MOVE_PX_PER_SEC * elapsed_sec
                self.move(self._loat_x, self.y())
        elif self.state == 2:
            if self.elapsed_stay_sec > STAY_TIME:
                self.state = 3
            else:
                self.elapsed_stay_sec += elapsed_sec
        else:
            if self.float_x >= HIDE_X:
                self.state = 0
                self.hide()
            else:
                self.float_x += MOVE_PX_PER_SEC * elapsed_sec
                self.move(self.float_x, self.y())

    def warn(self, title, msg):
        self.setText("<font color=\"orange\">" + title + "</font><br>" + msg)
        self.state = 1
        self.adjustSize()
        self.resize(self.width(), self.height() + HEIGHT_PAD)
        self.show()

    def error(self, title, msg):
        self.setText("<font color=\"red\">" + title + "</font><br>" + msg)
        self.state = 1
        self.adjustSize()
        self.resize(self.width(), self.height() + HEIGHT_PAD)
        self.show()
