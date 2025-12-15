from PyQt5.QtWidgets import QApplication
from StyleSheet import StyleSheet
from qt_classes.GUI import GUI
from petri_net.FridgePetriNet import fridge_pn
from threads.WorkerThread import WorkerThread


def main():

    fire_thread = WorkerThread(fridge_pn, interval=0.5)
    fire_thread.start()

    app = QApplication([])
    app.setStyleSheet(StyleSheet.App.value)
    window = GUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()