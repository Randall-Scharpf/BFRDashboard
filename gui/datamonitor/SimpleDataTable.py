from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from gui.datamonitor.DataLabel import DataLabel
import globalfonts as gf


class SimpleDataTable(QWidget):
    def __init__(self, parent=None):
        super(SimpleDataTable, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.titles = []
        self.labels = []

    def init(self, titles):
        for title in titles:
            self.titles.append(title)
            label = DataLabel(text=title+": N", word_wrap=True)
            self.labels.append(label)
            self.layout.addWidget(label)

    def update_values(self, values):
        for index, value in enumerate(values):
            self.labels[index].setText(self.titles[index] + ": " + value)
