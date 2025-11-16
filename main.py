from PyQt5.QtWidgets import QApplication
from StyleSheet import StyleSheet
from qt_classes.GUI import GUI

from petri_net.petriNet import Place, ArcOut, ArcIn, Transition, PetriNet

def main():
    print("=======INITIAL PETRI NET DEMONSTRATION========")
    p1 = Place("P1","p1_test",1)
    p2 = Place("P2","p2_test",4)
    p3 = Place("P3","p3_test",0)
    p4 = Place("P4", "p4_test", 0)

    a1 = ArcOut(p1,1)
    a2 = ArcOut(p2,2)
    a3 = ArcIn(p3,1)

    a4 = ArcOut(p3,1)
    a5 = ArcIn(p4,1)

    t1 = Transition([a1,a2], [a3], "T1")
    t2 = Transition([a4], [a5], "T2")

    p_net = PetriNet([t1, t2])

    print(p_net.get_current_description())
    while p_net.solve_one_iteration():
        print(p_net.get_current_description())

    app = QApplication([])
    app.setStyleSheet(StyleSheet.App.value)
    window = GUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
