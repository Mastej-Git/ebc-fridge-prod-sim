class CoolingSystem():

    def __init__(self, type: str, energy_class: str):
        self.is_activated = False
        self.type = type
        self.energy_class = energy_class

    def check_activation(self):
        if self.type is not None and self.energy_class is not None:
            self.is_activated = True

    def remove_parameters(self):
        self.type = None
        self.energy_class = None
        self.is_activated = False
