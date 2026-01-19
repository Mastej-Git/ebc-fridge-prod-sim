class Lights():

    def __init__(self, type: str, automatic: str):
        self.is_activated = False
        self.type = type
        self.automatic = automatic

    def check_activation(self):
        if self.type is not None and self.automatic is not None:
            self.is_activated = True

    def remove_parameters(self):
        self.type = None
        self.automatic = None
        self.is_activated = False