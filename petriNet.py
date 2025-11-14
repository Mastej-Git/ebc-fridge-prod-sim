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
        self.place.num_tokens += self.weight # Remove set number of tokens

class Transition:
    def __init__(self, out_arcs : list[ArcOut], in_arcs : list[ArcIn]):
        # self.in_arcs: list = out_arcs
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
    
    def solve_one_loop(self):
        for t in self.transitions:
            t.fire()


p1 = Place("P1","p1_test",1)
p2 = Place("P2","p2_test",4)
p3 = Place("P3","p3_test",0)

a1 = ArcOut(p1,1)
a2 = ArcOut(p2,2)
a3 = ArcIn(p3,1)

t1 = Transition([a1,a2], [a3])


p_net = PetriNet([t1])
p_net.solve_one_loop()

