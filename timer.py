import globalfonts
import logging
from PyQt5.QtCore import QDateTime


# constants
MS_PER_UPDATE = 10
ELAPSED_UPDATE_TOLERANCE = 1000
ELAPSED_UPDATE_MAX = 99 * 1000
# to be initialized before calling on_update_labels
main_win = None

elapsed_ms = 1000
elapsed_update_time = ELAPSED_UPDATE_TOLERANCE


def on_update_labels():
    global MS_PER_UPDATE, main_win, elapsed_ms, elapsed_update_time
    elapsed_ms += MS_PER_UPDATE
    elapsed_update_time += MS_PER_UPDATE

    # update Time Label every whole second
    if elapsed_ms > 1000:
        time = QDateTime.currentDateTime()
        time_display = time.toString('yy/MM/dd h:mm:ss AP dddd')
        main_win.TimeLabel.setText(time_display)
        elapsed_ms -= 1000

    # update CAN Hat Status
    global ELAPSED_UPDATE_TOLERANCE, ELAPSED_UPDATE_MAX
    if elapsed_update_time > ELAPSED_UPDATE_TOLERANCE:
        if elapsed_update_time > ELAPSED_UPDATE_MAX:
            elapsed_update_time = ELAPSED_UPDATE_MAX
        main_win.CANConnectionLabel.setText("No Connection (" + str(int(elapsed_update_time / 1000)) + ")")
        main_win.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + "color: red;" + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))
    else:
        main_win.CANConnectionLabel.setText("Connected")
        main_win.CANStatusLabel.setStyleSheet(globalfonts.FONT_CSS + "color: green;"  + globalfonts.TRANSPARENT_CSS + globalfonts.scaled_css_size(25))


def on_update_data():
    global elasped_update_time
    elapsed_update_time = 0
