from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from gui.datamonitor.DataLabel import DataLabel
import globalfonts as gf


class SimpleDataTable(QWidget):
    def __init__(self, parent=None):
        super(SimpleDataTable, self).__init__(parent)
        self.__layout = QVBoxLayout(self)
        self.__titles = []
        self.__labels = []

    def init(self, titles):
        for title in titles:
            self.__titles.append(title)
            label = DataLabel(text=title+": N", word_wrap=True)
            self.__labels.append(label)
            self.__layout.addWidget(label)

    def update_values(self, values):
        for index, value in enumerate(values):
            self.__labels[index].setText(self.__titles[index] + ": " + value)
