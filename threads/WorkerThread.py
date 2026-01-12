from PyQt5.QtCore import QThread, pyqtSignal
from petri_net.FridgePetriNet import fridge_pn1
import time

class WorkerThread(QThread):
    fired = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, available_tr, logger, interval=0.5, parent=None):
        super().__init__(parent)
        self.available_tr = available_tr
        self.logger = logger
        self.interval = interval
        self._running = True

    def run(self):
        tr_to_exec = []
        while self._running:

            if "T002" in self.available_tr:
                self.logger.add_log_entry(f"STARTED: Production of Fridge ID: .")
                fridge_pn1.fire_transition("T001")
                time.sleep(0.5)

            for transition in self.available_tr:
                if fridge_pn1.transitions[transition].is_enabled():
                    tr_to_exec.append(transition)

            for transition in tr_to_exec:
                if fridge_pn1.transitions[transition].is_enabled() and fridge_pn1.transitions[transition].can_fire():
                    fridge_pn1.fire_transition(transition)
                    self.available_tr.remove(transition)
            # for transition in self.available_tr:
            #     t = self.available_tr.transitions[transition]

            #     if t.is_enabled() and t.can_fire():
            #         self.available_tr.fire_transition(transition)
            #         print(self.available_tr)
            #         self.fired.emit(transition)
            time.sleep(self.interval)
        self.finished.emit()

    def stop(self):
        self._running = False
        self.wait()
