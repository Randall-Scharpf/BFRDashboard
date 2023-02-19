from PyQt5.QtCore import QRunnable, Qt, QThreadPool


class Receive(QRunnable):
    def __init__(self):
        super().__init__()
        self.keep_running = True

    def run(self):
        while self.keep_running:
            pass

    def stop(self):
        self.keep_running = False
