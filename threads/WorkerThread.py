from PyQt5.QtCore import QThread, pyqtSignal
import time

class WorkerThread(QThread):
    fired = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, fridge_pn, interval=0.5, parent=None):
        super().__init__(parent)
        self.fridge_pn = fridge_pn
        self.interval = interval
        self._running = True

    def run(self):
        while self._running:
            for transition in self.fridge_pn.transitions:
                t = self.fridge_pn.transitions[transition]

                if t.is_enabled() and t.can_fire():
                    self.fridge_pn.fire_transition(transition)
                    print(self.fridge_pn)
                    self.fired.emit(transition)
            time.sleep(self.interval)
        self.finished.emit()

    def stop(self):
        self._running = False
        self.wait()
