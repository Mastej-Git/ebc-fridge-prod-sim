from PyQt5.QtWidgets import (
    QMainWindow, 
    QTabWidget, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QFrame
)
from qt_classes.AnimatedButton import AnimatedButton
from qt_classes.GanttChart import GanttChart
from StyleSheet import StyleSheet
from elements.FileDialog import FileDialog

class GUI(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Tab Example")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QFrame()
        central_widget.setStyleSheet(StyleSheet.CentralWidget.value)
        layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        self.tabs.tabBar().setExpanding(True)
        self.tabs.setStyleSheet(StyleSheet.Tab.value)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Loaded elements")
        self.tabs.addTab(self.tab3, "Gantt tab")

        self.create_tab_content()
        layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

    def create_tab_content(self):
        sub_tab_widget = QTabWidget()
        sub_tab_widget.setTabPosition(QTabWidget.West)
        sub_tab_widget.setStyleSheet(StyleSheet.SubTab.value)

        self.create_dial_tab()        
        # layout1 = QVBoxLayout()
        # self.tab1.setLayout(layout1)

        layout2 = QVBoxLayout()
        self.tab2.setLayout(layout2)

        layout3 = QVBoxLayout()
        self.tab3.setLayout(layout3)

        self.create_gantt_tab()  # <-- dodajemy treść do taba 3

    def create_gantt_tab(self):
        layout = self.tab3.layout()
        if layout is None:
            layout = QVBoxLayout()
            self.tab3.setLayout(layout)

        example_tasks = [
            {"task": "Design", "start": 0, "end": 3},
            {"task": "Implementation", "start": 2, "end": 6},
            {"task": "Testing", "start": 5, "end": 8},
            {"task": "Deployment", "start": 7, "end": 9},
        ]
        gantt_widget = GanttChart(example_tasks)
        layout.addWidget(gantt_widget)
        
    def create_dial_tab(self):

        layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Wczytaj konfigurację")
        group_box1.setFixedHeight(200)

        label = QLabel("Nie wybrano żadnego pliku")

        hbox_layout = QHBoxLayout()
        vbox_layout = QVBoxLayout()

        read_file_button = AnimatedButton("Wczytaj")
        # read_file_button.clicked.connect(self.pb_read_json)

        self.file_dialog = FileDialog(label)

        chose_file_button = AnimatedButton("Wybierz plik")
        # chose_file_button.clicked.connect(self.pb_chose_file)

        vbox_layout.addWidget(chose_file_button)
        vbox_layout.addWidget(read_file_button)

        hbox_layout.addWidget(label)
        hbox_layout.addLayout(vbox_layout)

        group_box2 = QGroupBox("Panel kontrolny")
        group_box2.setFixedHeight(600)


        hbox_layout1 = QHBoxLayout()

        vbox_layout1 = QVBoxLayout()
        body_counter_label = self.create_label("Wczytanych korpusów: 0")
        production_counter_label = self.create_label("Korpusów w produkcji: 0")
        finished_bodys_label = self.create_label("Wyprodukowanych korpusów: 0")
        vbox_layout1.addWidget(body_counter_label)
        vbox_layout1.addWidget(production_counter_label)
        vbox_layout1.addWidget(finished_bodys_label)

        vbox_layout2 = QVBoxLayout()
        self.label_tmp = self.create_label("Brak wybranej ilości")
        vbox_layout2.addWidget(self.label_tmp)
        chose_value_button = AnimatedButton("Wybierz ilość")
        # chose_value_button.clicked.connect(self.pb_input_dialog)
        vbox_layout2.addWidget(chose_value_button)
        produce_button = AnimatedButton("Produkuj")
        # produce_button.clicked.connect(self.pb_produce)
        vbox_layout2.addWidget(produce_button)

        hbox_layout1.addLayout(vbox_layout1)
        hbox_layout1.addLayout(vbox_layout2)

        group_box2.setLayout(hbox_layout1)
        group_box1.setLayout(hbox_layout)

        layout1.addWidget(group_box2)
        layout1.addWidget(group_box1)
        self.tab1.setLayout(layout1)

    def create_label(self, label_str: str, maximuxm_height: int = 70) -> QLabel:
        label = QLabel(label_str)
        label.setStyleSheet(StyleSheet.QLabel.value)
        label.setMaximumHeight(maximuxm_height)
        return label
        