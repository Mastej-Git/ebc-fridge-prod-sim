import numpy as np

class Place:
    def __init__(self, name: str, description: str, token_num: int):
        self.name = name
        self.description = description
        self.num_tokens: int = token_num

class ArcBase:
    def __init__(self, place : Place, weight : int=1):
        self.place : Place = place
        self.weight : int = weight
       
class ArcOut(ArcBase): # FROM PLACE
    def trigger(self):
        self.place.num_tokens -= self.weight # Remove set number of tokens

    def can_trigger(self) -> bool:
        return self.place.num_tokens >= self.weight

class ArcIn(ArcBase): # TO PLACE
    def trigger(self):
        self.place.num_tokens += self.weight

class Transition:
    def __init__(self, out_arcs : list[ArcOut], in_arcs : list[ArcIn], name: str = None):
        # self.in_arcs: list = out_arcs
        self.name = name
        self.out_arcs: list[ArcOut] = out_arcs
        self.arcs = self.out_arcs + in_arcs

    def fire(self) -> bool:
        can_fire = all(arc.can_trigger() for arc in self.out_arcs) 

        if can_fire:
            for arc in self.arcs:
                arc.trigger()

        return can_fire


class PetriNet:
    def __init__(self, transitions: list[Transition] = None):
        self.transitions : list[Transition] = transitions
        self._places : dict[str, Place] = {} # Just for getting places through a name key

        # Build the places dictionary
        if transitions:
            for t in transitions:
                for arc in t.arcs:
                    if arc.place.name not in self._places:
                        self._places[arc.place.name] = arc.place

    def get_place(self, place_name: str) -> Place:
        return self._places.get(place_name)

    def solve_one_iteration(self) -> bool:
        """Can be used to iterate through the net until no firing options are available"""
        sth_fired : bool = False
        for t in self.transitions:
            if t.fire():
                sth_fired = True
        return sth_fired

    def get_current_description(self) -> str:
        description: str = ""
        for place in self._places.values():
            description += f'{place.name}:{place.num_tokens}; '
        return description



