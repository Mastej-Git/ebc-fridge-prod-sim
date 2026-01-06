class Doors():

    def __init__(self, material: str, machine: str, front_panel: bool):
        self.is_activated = False
        self.material = material
        self.machine = machine
        self.front_panel = front_panel

    def check_activation(self):
        if self.material is not None and self.machine is not None and self.front_panel is not None:
            self.is_activated = True

    def remove_parameters(self):
        self.material = None
        self.machine = None
        self.front_panel = None
        self.is_activated = False
