# This Python file uses the following encoding: utf-8
import sys
import resources  # https://www.pythonguis.com/tutorials/qresource-system/
import update
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QFile, QTimer, QDateTime


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        main_ui = QFile(":/res/main_ui")
        main_ui.open(QFile.ReadOnly)
        # run this command: pyrcc5 resources.qrc -o resources.py to package main_ui
        # uic.loadUi(main_ui, self)
        uic.loadUi("gui/main.ui", self)
        print(self.RPMDial.units)

        update.main_win = self
        update.ms_per_update = 10
        timer = QTimer(self)
        timer.timeout.connect(update.on_update_labels)
        timer.start(update.ms_per_update)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
