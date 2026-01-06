class Shelves():

    def __init__(self, material: str, number: str, adjustable: bool):
        self.is_activated = False
        self.material = material
        self.number = number
        self.adjustable = adjustable

    def check_activation(self):
        if self.material is not None and self.number is not None and self.adjustable is not None:
            self.is_activated = True

    def remove_parameters(self):
        self.material = None
        self.number = None
        self.adjustable = None
        self.is_activated = False
