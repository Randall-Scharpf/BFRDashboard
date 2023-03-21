from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from gui.datamonitor.DataLabel import DataLabel
import globalfonts as gf


DATA_NAMES = {'acc_x': "AccX", 'acc_y': "AccY", 'acc_z': "AccZ", 'acc_magnitude': "AccM", 'battery': "Battery (V)", 'brake': "Brake (%)",
'coolant': "Coolant Temp (F)", 'engine_speed': "Engine Speed (rpm)", 'exhaust': "Exhaust Temp (F)", 'fan1': "Fan (bool)", 'fuel_pressure': "FuelPre", 'fuel_pump': "FuelPump", 'gear': "Gear",
'ignition_timing': "IgnT", 'injector_duty': "InjD", 'intake': "IAT", 'lambda1': "Lambda", 'lambda_target': "LambdaT", 'log': "Log",
'lrt': "LRT", 'map': "MAP", 'mass_airflow': "MassAir", 'rotation_x': "RotX", 'rotation_y': "RotY", 'rotation_z': "RotZ",
'throttle': "Throttle (%)", 've': "VE", 'vehicle_speed': "Vehicle Speed (mph)"}
COL_NAMES = ["Value", "MPS"]
COL_WIDTH = [110, 70]
FONT_SIZE = 20


class DataTable(QWidget):
    data_labels = {}

    def __init__(self, parent=None):
        super(DataTable, self).__init__(parent)

    def init(self, keys):
        self.keys = keys
        self.layout = QGridLayout(self)
        # initialize first row (column names)
        for index, col_name in enumerate(COL_NAMES):
            self.layout.addWidget(DataLabel(text=col_name, fixed_width=COL_WIDTH[index]), 1, index + 2)
        # initialize first column (row names)
        for index, row_name in enumerate(keys):
            self.layout.addWidget(DataLabel(text=DATA_NAMES[row_name], word_wrap=True), index + 2, 1)
        for row, key in enumerate(keys):
            self.data_labels[key] = {}
            for col, col_name in enumerate(COL_NAMES):
                label = DataLabel(text="N", fixed_width=COL_WIDTH[col])
                self.layout.addWidget(label, row + 2, col + 2)
                self.data_labels[key][col_name] = label

    def update_frame(self, data_dict):
        for key in self.keys:
            data = data_dict[key]
            if data['prev_update_ts'] != -1:
                self.data_labels[key]['Value'].set_number(data['value'])
                if data['mps'] != -1:
                    self.data_labels[key]['MPS'].set_number(int(data['mps']))
