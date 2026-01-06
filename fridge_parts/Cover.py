class Cover():

    def __init__(self, material: str, color: str):
        self.is_activated = False
        self.material = material
        self.color = color

    def check_activation(self):
        if self.material is not None and self.color is not None:
            self.is_activated = True

    def remove_parameters(self):
        self.material = None
        self.color = None
        self.is_activated = False
