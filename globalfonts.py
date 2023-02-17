SCALE = 1.0
DIAL_SCALE = 1.0


def scaled_css_size(px):
    return "font-size:" + str(int(px * SCALE)) + "px;"


def scaled_dial_size(size):
    return size * DIAL_SCALE


def scale_size_for_all(main_win):
    main_win.CANStatusLabel.setStyleSheet("color: white; background-color : rgba(0, 0, 0, 0)" + scaled_css_size(25))
    main_win.CANConnectionLabel.setStyleSheet("color: white; background-color : rgba(0, 0, 0, 0)" + scaled_css_size(25))
    main_win.TimeLabel.setStyleSheet("color: white; background-color : rgba(0, 0, 0, 0)" + scaled_css_size(25))
    main_win.LogLabel.setStyleSheet("color: white; background-color : rgba(0, 0, 0, 0)" + scaled_css_size(25))
    main_win.AFRLabel.setStyleSheet("color: #CEF4FF; background-color:rgba(0,0,0,0);" + scaled_css_size(35))
    main_win.RPMLabel.setStyleSheet("color: #CEF4FF;background-color:rgba(0,0,0,0);" + scaled_css_size(40))
    main_win.VelocityLabel.setStyleSheet("color: #CEF4FF;background-color:rgba(0,0,0,0);" + scaled_css_size(35))
