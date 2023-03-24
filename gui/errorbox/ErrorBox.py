from PyQt5.QtWidgets import QLabel


# left-most x for the error box to go
SHOW_X = 1100
# right-most x for the error box to go
HIDE_X = 1260
# speed of moving
MOVE_PX_PER_SEC = 200
# how many seconds it stays unmoving on the screen
STAY_TIME = 5
# increase the height by a little to make the lines look centered
HEIGHT_PAD = 10


class ErrorBox(QLabel):
    def __init__(self, parent=None):
        super(ErrorBox, self).__init__(parent)
        # state of its motion
        # 0: hide and do nothing, 1: slide into the screen, 2: stay for a period of time, 3: slide back
        self.state = 0
        # keeps track of how long it has stayed unmoving during state 2
        self.elapsed_stay_sec = 0
        # current x position, but in float
        # if we just use self.x(), because it's an int the motion looks unsmooth
        self.float_x = HIDE_X
        self.setFixedWidth(160)
        self.hide()

    def update_frame(self, elapsed_sec):
        # do nothing
        if self.state == 0:
            return
        # slide into the screen
        elif self.state == 1:
            if self.float_x <= SHOW_X:
                self.state = 2
                self.elapsed_stay_sec = 0
            else:
                self.float_x -= MOVE_PX_PER_SEC * elapsed_sec
                self.move(self.float_x, self.y())
        # stay unmoving
        elif self.state == 2:
            if self.elapsed_stay_sec > STAY_TIME:
                self.state = 3
            else:
                self.elapsed_stay_sec += elapsed_sec
        # slide back to hide self
        else:
            if self.float_x >= HIDE_X:
                self.state = 0
                self.hide()
            else:
                self.float_x += MOVE_PX_PER_SEC * elapsed_sec
                self.move(self.float_x, self.y())

    def warn(self, title, msg):
        try:
            self.setText("<font color=\"orange\">" + title + "</font><br>" + msg)
            self.state = 1
            self.adjustSize()
            self.resize(self.width(), self.height() + HEIGHT_PAD)
            self.show()
        except Exception as e:
            print("Error at ErrorBox.warn()")
            print("title=" + str(title) + ", msg=" + str(msg))
            print(traceback.format_exc())

    def error(self, title, msg):
        try:
            self.setText("<font color=\"red\">" + title + "</font><br>" + msg)
            self.state = 1
            self.adjustSize()
            self.resize(self.width(), self.height() + HEIGHT_PAD)
            self.show()
        except Exception as e:
            print("Error at ErrorBox.error()")
            print("title=" + str(title) + ", msg=" + str(msg))
            print(traceback.format_exc())
