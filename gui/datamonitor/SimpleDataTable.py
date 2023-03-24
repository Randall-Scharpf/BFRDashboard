from PyQt5.QtWidgets import QWidget, QVBoxLayout
from gui.datamonitor.DataLabel import DataLabel


# a helper table that displays a column of labels
class SimpleDataTable(QWidget):
    def __init__(self, parent=None):
        super(SimpleDataTable, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        # the unchanged title of the data, everything before the ':'
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
