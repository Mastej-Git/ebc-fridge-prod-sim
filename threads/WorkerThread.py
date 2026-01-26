from PyQt5.QtCore import QThread, pyqtSignal
from petri_net.FridgePetriNet import fridge_pn1
import time

class WorkerThread(QThread):
    fired = pyqtSignal(str)
    finished = pyqtSignal()
    fridge_finished = pyqtSignal()

    def __init__(self, available_tr, logger, fridge_pord_params, control_tab, interval=0.5, parent=None):
        super().__init__(parent)
        self.available_tr = available_tr
        self.logger = logger
        self.fridge_prod_params = fridge_pord_params
        self.interval = interval
        self.control_tab = control_tab
        self._running = True

    def run(self):
        while self._running:
            tr_to_remove = []
            for transition in list(self.available_tr):
                try:
                    if transition in fridge_pn1.transitions:
                        t = fridge_pn1.transitions[transition]
                        if t.is_enabled() and t.can_fire():
                            fridge_pn1.fire_transition(transition)
                            # print(f"FIRED: Transition: {transition}")
                            tr_to_remove.append(transition)
                except Exception as e:
                    print(f"Error firing {transition}: {e}")
            
            for transition in tr_to_remove:
                if transition in self.available_tr:
                    self.available_tr.remove(transition)

                if transition == "T903":
                    self.fridge_prod_params['finished'] += 1
                    self.fridge_prod_params['in_prod'] -= 1
                    self.control_tab.finished_bodys_label.setText(f"Manufactured fridges: {self.fridge_prod_params['finished']}")
                    self.control_tab.production_counter_label.setText(f"Fridges in production: {self.fridge_prod_params['in_prod']}")
                    self.fridge_finished.emit()
                    
                    
            time.sleep(self.interval)
        self.finished.emit()

    def stop(self):
        self._running = False
        self.wait()
