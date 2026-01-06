from fridge_parts.Cover import Cover
from fridge_parts.Doors import Doors
from fridge_parts.Shelves import Shelves
from fridge_parts.CoolingSystem import CoolingSystem
from fridge_parts.Lights import Lights

class Fridge():

    def __init__(
        self, body_id: int,
        cover: Cover,
        doors: Doors,
        shelves: Shelves,
        cooling_system: CoolingSystem,
        lights: Lights
    ):
        self.body_id = body_id

        self.cover = cover
        self.doors = doors
        self.shelves = shelves
        self.cooling_system = cooling_system
        self.lights = lights

    def remove_parameters(self) -> None:
        self.cover.remove_parameters()
        self.doors.remove_parameters()
        self.shelves.remove_parameters()
        self.cooling_system.remove_parameters()
        self.lights.remove_parameters()

    def check_parts_activation(self) -> None:
        self.cover.check_activation()
        self.doors.check_activation()
        self.shelves.check_activation()
        self.cooling_system.check_activation()
        self.lights.check_activation()

    def is_ready(self) -> bool:
        if (
        self.cover.is_activated and
        self.doors.is_activated and
        self.shelves.is_activated and
        self.cooling_system.is_activated and
        self.lights.is_activated
        ):
            return True
        return False
