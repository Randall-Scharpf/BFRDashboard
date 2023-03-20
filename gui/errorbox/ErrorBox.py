from PyQt5.QtWidgets import QLabel


SHOW_X = 1100
HIDE_X = 1260
MOVE_PX_PER_SEC = 200
STAY_TIME = 5


class ErrorBox(QLabel):
    # 0: hide and do nothing, 1: slide into the screen, 2: stay for a period of time, 3: slide back
    __state = 0
    __elapsed_stay_sec = 0
    __float_x = HIDE_X

    def __init__(self, parent=None):
        super(ErrorBox, self).__init__(parent)
        self.setFixedWidth(160)
        self.hide()

    def update_frame(self, elapsed_sec):
        if self.__state == 0:
            return
        elif self.__state == 1:
            if self.__float_x <= SHOW_X:
                self.__state = 2
                self.__elapsed_stay_sec = 0
            else:
                self.__float_x -= MOVE_PX_PER_SEC * elapsed_sec
                self.move(self.__float_x, self.y())
        elif self.__state == 2:
            if self.__elapsed_stay_sec > STAY_TIME:
                self.__state = 3
            else:
                self.__elapsed_stay_sec += elapsed_sec
        else:
            if self.__float_x >= HIDE_X:
                self.__state = 0
                self.hide()
            else:
                self.__float_x += MOVE_PX_PER_SEC * elapsed_sec
                self.move(self.__float_x, self.y())

    def warn(self, title, msg):
        self.setText("<font color=\"orange\">" + title + "</font><br>" + msg)
        self.__state = 1
        self.adjustSize()
        self.show()

    def error(self, title, msg):
        self.setText("<font color=\"red\">" + title + "</font><br>" + msg)
        self.__state = 1
        self.adjustSize()
        self.show()
