from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from gui.datamonitor.DataLabel import DataLabel
import globalfonts as gf


DATA_NAMES = {'acc_x': "AccX (g)", 'acc_y': "AccY (g)", 'acc_z': "AccZ (g)", 'acc_magnitude': "AccM (g)", 'battery': "Bat (V)", 'brake': "Brake (%)",
'coolant': "Cool (F)", 'engine_speed': "ESpd (rpm)", 'exhaust': "EGT (F)", 'fan1': "Fan (bool)", 'fuel_pressure': "FPres (PSIg)", 'fuel_pump': "FPump (bool)", 'gear': "Gear",
'ignition_timing': "IgnT (Deg)", 'injector_duty': "InjD (%)", 'intake': "IAT (F)", 'lambda1': "Lambda", 'lambda_target': "LambdaT", 'log': "Log",
'lrt': "LRT (ms)", 'map': "MAP (kPa)", 'mass_airflow': "MAir (gms/s)", 'rotation_x': "RotX (deg/s)", 'rotation_y': "RotY (deg/s)", 'rotation_z': "RotZ (deg/s)",
'throttle': "Throt (%)", 've': "VE (%)", 'vehicle_speed': "VSpd (mph)"}
COL_NAMES = ["Value", "Obs", "MPS"]
COL_WIDTH = [90, 60, 60]  # min 80, 50, 50
FONT_SIZE = 20


class DataTable(QWidget):
    def __init__(self, parent=None):
        super(DataTable, self).__init__(parent)
        self.__layout = QGridLayout(self)
        self.__data_labels = {}

    def init(self, keys):
        self.keys = keys
        # initialize first row (column names)
        for index, col_name in enumerate(COL_NAMES):
            self.__layout.addWidget(DataLabel(text=col_name, fixed_width=COL_WIDTH[index]), 1, index + 2)
        # initialize first column (row names)
        for index, row_name in enumerate(keys):
            self.__layout.addWidget(DataLabel(text=DATA_NAMES[row_name], word_wrap=True), index + 2, 1)
        for row, key in enumerate(keys):
            self.__data_labels[key] = {}
            for col, col_name in enumerate(COL_NAMES):
                label = DataLabel(text="N", fixed_width=COL_WIDTH[col])
                self.__layout.addWidget(label, row + 2, col + 2)
                self.__data_labels[key][col_name] = label

    def update_frame(self, data_dict):
        for key in self.keys:
            data = data_dict[key]
            if data['prev_update_ts'] != -1:
                self.__data_labels[key]['Value'].set_number(data['value'])
                if data['mps'] != -1:
                    self.__data_labels[key]['MPS'].set_number(int(data['mps']))
                    self.__data_labels[key]['Obs'].set_number(max(-99, min(99, data['obs'])))
