import globalfonts
import logging
from PyQt5.QtCore import QDateTime


# constants
MS_PER_UPDATE = 100 # 100 for RP
ELAPSED_UPDATE_TOLERANCE = 1000
ELAPSED_UPDATE_MAX = 99 * 1000


class UpdateTimer():
    def __init__(self, main_win):
        self.main_win = main_win
        self.elapsed_ms = 1000
        self.elapsed_update_time = ELAPSED_UPDATE_TOLERANCE

    def on_update_labels(self):
        global MS_PER_UPDATE
        self.elapsed_ms += MS_PER_UPDATE
        self.elapsed_update_time += MS_PER_UPDATE

        # update Time Label every whole second
        if self.elapsed_ms > 1000:
            time = QDateTime.currentDateTime()
            time_display = time.toString('MM/dd/yy h:mm:ss AP dddd')
            self.main_win.TimeLabel.setText(time_display)
            self.elapsed_ms -= 1000

        # update CAN Hat Status
        global ELAPSED_UPDATE_TOLERANCE, ELAPSED_UPDATE_MAX
        if self.elapsed_update_time > ELAPSED_UPDATE_TOLERANCE:
            if self.elapsed_update_time > ELAPSED_UPDATE_MAX:
                self.elapsed_update_time = ELAPSED_UPDATE_MAX
            self.main_win.CANConnectionLabel.setText("No Connection (" + str(int(self.elapsed_update_time / 1000)) + ")")
            self.main_win.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + "color: red;" + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))
        else:
            self.main_win.CANConnectionLabel.setText("Connected")
            self.main_win.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + "color: green;"  + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))


    def on_receive_data(self):
        self.elapsed_update_time = 0

