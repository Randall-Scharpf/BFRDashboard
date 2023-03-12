import globalfonts
from datetime import datetime


MS_PER_UPDATE = 100
ELAPSED_UPDATE_TOLERANCE = 1000
ELAPSED_UPDATE_MAX = 99 * 1000
FPS_UPDATE_TIME = 500

USE_SYS_TIME = True
TIME_DISPLAY_FORMAT = '%m/%d/%y %I:%M:%S %p %a'


class UpdateTimer():
    timestamp = -1

    __elapsed_timer_ms = 1000
    __elapsed_update_time = ELAPSED_UPDATE_TOLERANCE
    __elasped_update_fps_time = FPS_UPDATE_TIME
    __elapsed_num_messages = 0
    __prev_disconnection = -2

    def __init__(self, main_win):
        self.main_win = main_win

    def on_update_labels(self):
        global MS_PER_UPDATE
        self.__elapsed_timer_ms += MS_PER_UPDATE
        self.__elapsed_update_time = min(MS_PER_UPDATE + self.__elapsed_update_time, ELAPSED_UPDATE_MAX)
        self.__elasped_update_fps_time += MS_PER_UPDATE

        # update Time Label every whole second
        if self.__elapsed_timer_ms > 1000:
            if USE_SYS_TIME or self.timestamp == -1:
                time_display = datetime.now().strftime('(ST) ' + TIME_DISPLAY_FORMAT)
            else:
                time_display = datetime.fromtimestamp(self.timestamp).strftime(TIME_DISPLAY_FORMAT)
            self.main_win.TimeLabel.setText(time_display)
            self.__elapsed_timer_ms -= 1000

        # update CAN Hat Status
        global ELAPSED_UPDATE_TOLERANCE
        if self.__elapsed_update_time > ELAPSED_UPDATE_TOLERANCE:
            disconnection_time = int(self.__elapsed_update_time / 1000)
            if self.__prev_disconnection != disconnection_time:
                self.main_win.CANConnectionLabel.setText('No Connection (' + str(disconnection_time) + ')')
                self.main_win.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + 'color: red;' + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))
                self.__prev_disconnection = disconnection_time
        else:
            if self.__prev_disconnection != -1:
                self.main_win.CANConnectionLabel.setText('Connected')
                self.main_win.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + 'color: green;'  + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))
                self.__prev_disconnection = -1

        # update FPS label
        global FPS_UPDATE_TIME
        if self.__elasped_update_fps_time > FPS_UPDATE_TIME:
            self.main_win.FPSLabel.setText("FPS: " + str(min(999, int(self.__elapsed_num_messages * 1000 / FPS_UPDATE_TIME))))
            self.__elapsed_num_messages = 0
            self.__elasped_update_fps_time = 0

    def on_receive_data(self):
        self.__elapsed_update_time = 0
        self.__elapsed_num_messages += 1
