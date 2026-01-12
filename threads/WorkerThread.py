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
        while self._running:
            if "T002" in self.available_tr:
                self.logger.add_entry("STARTED: Production of Fridge.")
                print("STARTED: Production of Fridge.")
                fridge_pn1.fire_transition("T001")
                time.sleep(0.5)

            tr_to_remove = []
            for transition in list(self.available_tr):
                try:
                    if transition in fridge_pn1.transitions:
                        t = fridge_pn1.transitions[transition]
                        if t.is_enabled() and t.can_fire():
                            fridge_pn1.fire_transition(transition)
                            print(f"FIRED: Transition: {transition}")
                            tr_to_remove.append(transition)
                except Exception as e:
                    print(f"Error firing {transition}: {e}")
            
            for transition in tr_to_remove:
                if transition in self.available_tr:
                    self.available_tr.remove(transition)

                if transition == "T903":
                    print(f"FINISHED: Fridge: {transition}")
                    
                    
            time.sleep(self.interval)
        self.finished.emit()

    def stop(self):
        self._running = False
        self.wait()
