import globalfonts
from datetime import datetime


# constants
MS_PER_UPDATE = 100 # 100 for RP
ELAPSED_UPDATE_TOLERANCE = 1000
ELAPSED_UPDATE_MAX = 99 * 1000
FPS_UPDATE_TIME = 500

TIME_DISPLAY_FORMAT = '%m/%d/%y %I:%M:%S %p %a'


class UpdateTimer():
    elapsed_num_messages = 0
    timestamp = -1

    def __init__(self, main_win):
        self.main_win = main_win
        self.elapsed_ms = 1000
        self.elapsed_update_time = ELAPSED_UPDATE_TOLERANCE
        self.elasped_update_fps_time = FPS_UPDATE_TIME

    def on_update_labels(self):
        global MS_PER_UPDATE
        self.elapsed_ms += MS_PER_UPDATE
        self.elapsed_update_time += MS_PER_UPDATE
        self.elasped_update_fps_time += MS_PER_UPDATE

        # update Time Label every whole second
        if self.elapsed_ms > 1000:
            if self.timestamp == -1:
                time_display = datetime.now().strftime('(ST) ' + TIME_DISPLAY_FORMAT)
            else:
                time_display = datetime.fromtimestamp(self.timestamp).strftime(TIME_DISPLAY_FORMAT)
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

        # update FPS label
        if self.elasped_update_fps_time > FPS_UPDATE_TIME:
            self.main_win.FPSLabel.setText("FPS: " + str(min(999, int(self.elapsed_num_messages * 1000 / FPS_UPDATE_TIME))))
            self.elapsed_num_messages = 0
            self.elasped_update_fps_time = 0


    def on_receive_data(self):
        self.elapsed_update_time = 0
        self.elapsed_num_messages = self.elapsed_num_messages + 1


    def set_timestamp(self, ts):
        self.timestamp = ts

