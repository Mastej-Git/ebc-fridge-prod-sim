from PyQt5.QtCore import QThread, pyqtSignal

class Listener(QThread):
    fired = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, fridge_pn, interval=0.5, parent=None):
        super().__init__(parent)
        self.fridge_pn = fridge_pn
        self.interval = interval
        self._running = True

    def run(self):
        while self._running:
            pass
        self.finished.emit()

    def stop(self):
        self._running = False
        self.wait()

    # def update_available_tr(self, body: Body)