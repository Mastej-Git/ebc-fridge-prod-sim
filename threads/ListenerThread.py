from PyQt5.QtCore import QThread, pyqtSignal
from fridge_parts.Fridge import Fridge
from fridge_parts.FridgeAttributes import FridgeAttributes

class Listener(QThread):
    fired = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, available_tr, interval=0.5, parent=None):
        super().__init__(parent)
        # self.fridge_pn = fridge_pn
        self.interval = interval
        self._running = True

        self.body_counter = 0
        self.started_bodys = 0
        self.available_tr = available_tr

    def run(self):
        while self._running:
            pass
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

    def define_available_tr(self, av_fridge_trs: list, fridge: Fridge) -> list[str]:

        if fridge.cover.color == FridgeAttributes.Cover.Color.RED:
            av_fridge_trs.extend(["T105", "T108"])
        elif fridge.cover.color == FridgeAttributes.Cover.Color.GREEN:
            av_fridge_trs.extend(["T106", "T109"])
        elif fridge.cover.color == FridgeAttributes.Cover.Color.GREEN:
            av_fridge_trs.extend(["T107", "T110"])

        av_fridge_trs.extend(["T201", "T202", "T203", "T204"])
        if fridge.doors.machine == FridgeAttributes.Doors.Machine.ICE:
            av_fridge_trs.extend(["T205", "T207"])
        elif fridge.doors.machine == FridgeAttributes.Doors.Machine.WATER:
            av_fridge_trs.extend(["T206", "T208"])
        if fridge.doors.front_panel == FridgeAttributes.Doors.FrontPanel.YES:
            av_fridge_trs.extend(["T209", "T211"])
        elif fridge.doors.front_panel == FridgeAttributes.Doors.FrontPanel.NO:
            av_fridge_trs.extend(["T210"])

        av_fridge_trs.extend(["T301", "T302"])
        if fridge.shelves.quantity == FridgeAttributes.Shelves.Quantity.SIX:
            av_fridge_trs.extend(["T303", "T306"])
        elif fridge.shelves.quantity == FridgeAttributes.Shelves.Quantity.SEVEN:
            av_fridge_trs.extend(["T304", "T307"])
        elif fridge.shelves.quantity == FridgeAttributes.Shelves.Quantity.EIGHT:
            av_fridge_trs.extend(["T305", "T308"])
        if fridge.shelves.adjustable == FridgeAttributes.Shelves.Adjustable.YES:
            av_fridge_trs.extend(["T309", "T311"])
        elif fridge.shelves.adjustable == FridgeAttributes.Shelves.Adjustable.NO:
            av_fridge_trs.extend(["T310", "T312"])
        av_fridge_trs.extend(["T313", "T314", "T315"])

        av_fridge_trs.extend(["T401", "T402"])
        if fridge.cooling_system.type == FridgeAttributes.CoolingSystem.Type.NOFROST:
            av_fridge_trs.extend(["T403", "T406"])
        elif fridge.cooling_system.type == FridgeAttributes.CoolingSystem.Type.FROSTFREE:
            av_fridge_trs.extend(["T404", "T407"])
        elif fridge.cooling_system.type == FridgeAttributes.CoolingSystem.Type.STATIC:
            av_fridge_trs.extend(["T405", "T408"])
        av_fridge_trs.extend(["T409", "T410"])
        if fridge.cooling_system.energy_class == FridgeAttributes.CoolingSystem.EnergyClass.APPP:
            av_fridge_trs.extend(["T411", "T414"])
        elif fridge.cooling_system.energy_class == FridgeAttributes.CoolingSystem.EnergyClass.AP:
            av_fridge_trs.extend(["T412", "T415"])
        elif fridge.cooling_system.energy_class == FridgeAttributes.CoolingSystem.EnergyClass.B:
            av_fridge_trs.extend(["T413", "T416"])
        av_fridge_trs.extend(["T417"])

        av_fridge_trs.extend(["T501", "T502"])
        if fridge.lights.automatic == FridgeAttributes.Lights.Automatic.YES:
            av_fridge_trs.extend(["T503", "T505"])
        elif fridge.lights.automatic == FridgeAttributes.Lights.Automatic.NO:
            av_fridge_trs.extend(["T504", "T506"])
        if fridge.lights.type == FridgeAttributes.Lights.Type.LED:
            av_fridge_trs.extend(["T507", "T509"])
        elif fridge.lights.type == FridgeAttributes.Lights.Type.FLUORESCENT:
            av_fridge_trs.extend(["T508", "T510"])
        av_fridge_trs.extend(["T511"])
        
