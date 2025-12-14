from petri_net.PetriNet import PetriNet

fridge_pn = PetriNet()

time_unit = 1000

fridge_pn.add_place("P000", "Miejsce 1", tokens=0, ready_tokens=1, max_tokens=2, cooldown_ms=int(1.0*time_unit))
fridge_pn.add_place("P001", "Miejsce 2", tokens=0, ready_tokens=0, max_tokens=2, cooldown_ms=int(1.0*time_unit))
fridge_pn.add_place("P002", "Miejsce 2", tokens=0, ready_tokens=0, max_tokens=2, cooldown_ms=int(1.0*time_unit))
fridge_pn.add_place("P003", "Miejsce 3", tokens=0, ready_tokens=0, max_tokens=2, cooldown_ms=int(1.0*time_unit))


fridge_pn.add_transition("T001", {"P003": 1}, {"P000": 1})
fridge_pn.add_transition("T002", {"P000": 1}, {"P001": 1})
fridge_pn.add_transition("T003", {"P001": 1}, {"P002": 1})
fridge_pn.add_transition("T004", {"P002": 1}, {"P003": 1})
