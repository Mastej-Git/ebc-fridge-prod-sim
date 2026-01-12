from PyQt5.QtCore import QThread, pyqtSignal
from fridge_parts.Fridge import Fridge
import time

class Listener(QThread):
    fired = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, available_tr, set_for_prod, interval=0.5, parent=None):
        super().__init__(parent)
        self.interval = interval
        self._running = True

        self.body_counter = 0
        self.started_bodys = 0
        self.available_tr = available_tr
        self.set_for_prod = set_for_prod

    def run(self):
        while self._running:
            if len(self.set_for_prod) != 0:
                self.update_available_tr(self.set_for_prod.pop(0))
            time.sleep(self.interval)
        self.finished.emit()

    def stop(self):
        self._running = False
        self.wait()

    def update_available_tr(self, fridge: Fridge):
        self.body_counter += 1

        av_fridge_trs = []
        av_fridge_trs.extend(["T002", "T003"])
        self.define_available_tr(av_fridge_trs, fridge)
        av_fridge_trs.extend(["T901", "T902", "T903"])
        
        self.available_tr.extend(av_fridge_trs)

    def define_available_tr(self, av_fridge_trs: list, fridge: Fridge) -> list[str]:
        av_fridge_trs.extend(["T101", "T102", "T103", "T104"])
        color = fridge.cover.color.lower() if isinstance(fridge.cover.color, str) else str(fridge.cover.color).lower()
        if color == "red":
            av_fridge_trs.extend(["T105", "T108"])
        elif color == "green":
            av_fridge_trs.extend(["T106", "T109"])
        elif color == "blue":
            av_fridge_trs.extend(["T107", "T110"])
        av_fridge_trs.extend(["T111"])

        av_fridge_trs.extend(["T201", "T202", "T203", "T204"])
        machine = fridge.doors.machine.lower() if isinstance(fridge.doors.machine, str) else str(fridge.doors.machine).lower()
        if machine == "ice":
            av_fridge_trs.extend(["T205", "T207"])
        elif machine == "water":
            av_fridge_trs.extend(["T206", "T208"])
        
        front_panel = fridge.doors.front_panel
        if front_panel is True or str(front_panel).lower() == "true":
            av_fridge_trs.extend(["T209", "T211"])
        else:
            av_fridge_trs.extend(["T210"])
        av_fridge_trs.extend(["T212"])

        av_fridge_trs.extend(["T301", "T302"])
        quantity = int(fridge.shelves.quantity) if fridge.shelves.quantity else 0
        if quantity == 6:
            av_fridge_trs.extend(["T303", "T306"])
        elif quantity == 7:
            av_fridge_trs.extend(["T304", "T307"])
        elif quantity == 8:
            av_fridge_trs.extend(["T305", "T308"])
        
        adjustable = fridge.shelves.adjustable
        if adjustable is True or str(adjustable).lower() == "true":
            av_fridge_trs.extend(["T309", "T311"])
        else:
            av_fridge_trs.extend(["T310", "T312"])
        av_fridge_trs.extend(["T313", "T314", "T315"])

        av_fridge_trs.extend(["T401", "T402"])
        cooling_type = fridge.cooling_system.type.lower().replace("-", "") if isinstance(fridge.cooling_system.type, str) else str(fridge.cooling_system.type).lower()
        if cooling_type in ["nofrost", "no frost"]:
            av_fridge_trs.extend(["T403", "T406"])
        elif cooling_type in ["frostfree", "frost free"]:
            av_fridge_trs.extend(["T404", "T407"])
        elif cooling_type == "static":
            av_fridge_trs.extend(["T405", "T408"])
        av_fridge_trs.extend(["T409", "T410"])
        
        energy_class = fridge.cooling_system.energy_class if isinstance(fridge.cooling_system.energy_class, str) else str(fridge.cooling_system.energy_class)
        if energy_class == "A+++":
            av_fridge_trs.extend(["T411", "T414"])
        elif energy_class == "A+":
            av_fridge_trs.extend(["T412", "T415"])
        elif energy_class == "B":
            av_fridge_trs.extend(["T413", "T416"])
        av_fridge_trs.extend(["T417"])

        av_fridge_trs.extend(["T501", "T502"])
        automatic = fridge.lights.automatic
        if automatic is True or str(automatic).lower() == "true":
            av_fridge_trs.extend(["T503", "T505"])
        else:
            av_fridge_trs.extend(["T504", "T506"])
        
        light_type = fridge.lights.type.lower() if isinstance(fridge.lights.type, str) else str(fridge.lights.type).lower()
        if light_type == "led":
            av_fridge_trs.extend(["T507", "T509"])
        elif light_type == "fluorescent":
            av_fridge_trs.extend(["T508", "T510"])
        av_fridge_trs.extend(["T511"])

