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

fridge_pn1 = PetriNet()


fridge_pn1.add_place("P000", "Fridge order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P001", "Machine preparation", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.5*time_unit))

fridge_pn1.add_place("P100", "Cover order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P101", "Materials preparation", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(1*time_unit))
fridge_pn1.add_place("P102", "Forming order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.5*time_unit))
fridge_pn1.add_place("P103", "Cutting and forming", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(3*time_unit))
fridge_pn1.add_place("P104", "Painting order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P105", "Painting red", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(4*time_unit))
fridge_pn1.add_place("P106", "Painting green", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(4*time_unit))
fridge_pn1.add_place("P107", "Painting blue", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(4*time_unit))
fridge_pn1.add_place("P108", "Ready painted cover", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.5*time_unit))
fridge_pn1.add_place("P109", "Ready cover", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P110", "Machine M1 -- cutting", tokens=0, ready_tokens=1, max_tokens=1, cooldown_ms=int(0.1*time_unit))
fridge_pn1.add_place("P111", "Machine M2 -- painting", tokens=0, ready_tokens=1, max_tokens=1, cooldown_ms=int(0.1*time_unit))

fridge_pn1.add_place("P200", "Doors order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P201", "Materials preparation", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(1*time_unit))
fridge_pn1.add_place("P202", "Forming order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.5*time_unit))
fridge_pn1.add_place("P203", "Cutting and forming", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(3*time_unit))
fridge_pn1.add_place("P204", "Machine order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P205", "Ice machine installation", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(4*time_unit))
fridge_pn1.add_place("P206", "Water machine installation", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(4*time_unit))
fridge_pn1.add_place("P207", "Front panel order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P208", "Installing front panel", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(3*time_unit))
fridge_pn1.add_place("P209", "Ready installed machine", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.5*time_unit))
fridge_pn1.add_place("P210", "Ready doors", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P211", "Machine M3 -- cutting and forming the doors", tokens=0, ready_tokens=1, max_tokens=1, cooldown_ms=int(0.1*time_unit))
fridge_pn1.add_place("P212", "Machine M4 -- Machine installation", tokens=0, ready_tokens=1, max_tokens=1, cooldown_ms=int(0.1*time_unit))
fridge_pn1.add_place("P213", "Machine M5 -- Front panel installation", tokens=0, ready_tokens=1, max_tokens=1, cooldown_ms=int(0.1*time_unit))

fridge_pn1.add_place("P300", "Doors order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P301", "Materials preparation", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(1*time_unit))
fridge_pn1.add_place("P302", "Shelves quantity order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(3*time_unit))
fridge_pn1.add_place("P303", "Quantity 6", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.5*time_unit))
fridge_pn1.add_place("P304", "Quantity 7", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.5*time_unit))
fridge_pn1.add_place("P305", "Quantity 8", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.5*time_unit))
fridge_pn1.add_place("P306", "Adjustable height order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P307", "Adjustable height", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(2*time_unit))
fridge_pn1.add_place("P308", "No adjustable height", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.5*time_unit))
fridge_pn1.add_place("P309", "Forming order", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P310", "Cutting and forming", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(5*time_unit))
fridge_pn1.add_place("P311", "Ready formed shelves", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.5*time_unit))
fridge_pn1.add_place("P312", "Ready doors", tokens=0, ready_tokens=0, max_tokens=50, cooldown_ms=int(0.3*time_unit))
fridge_pn1.add_place("P313", "Machine M6 -- cutting and forming the order", tokens=0, ready_tokens=1, max_tokens=1, cooldown_ms=int(0.1*time_unit))


