from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox
)
from qt_classes.AnimatedButton import AnimatedButton
from StyleSheet import StyleSheet


class ControlTab(QWidget):
    def __init__(self):
        super().__init__()
        self.config_label = None
        self.body_counter_label = None
        self.production_counter_label = None
        self.finished_bodys_label = None
        self.label_tmp = None
        self.init_ui()

    def init_ui(self):
        layout1 = QVBoxLayout()

        # Load configuration group
        group_box1 = QGroupBox("Load configuration")
        group_box1.setFixedHeight(200)

        label = QLabel("No file selected")
        self.config_label = label

        hbox_layout = QHBoxLayout()
        vbox_layout = QVBoxLayout()

        read_file_button = AnimatedButton("Load")
        chose_file_button = AnimatedButton("Chose a file")

        vbox_layout.addWidget(chose_file_button)
        vbox_layout.addWidget(read_file_button)

        hbox_layout.addWidget(label)
        hbox_layout.addLayout(vbox_layout)
        group_box1.setLayout(hbox_layout)

        # Control panel group
        group_box2 = QGroupBox("Control panel")
        group_box2.setFixedHeight(600)

        hbox_layout1 = QHBoxLayout()
        vbox_layout1 = QVBoxLayout()

        self.body_counter_label = self.create_label("Loaded bodies: 0")
        self.production_counter_label = self.create_label("Bodies in production: 0")
        self.finished_bodys_label = self.create_label("Manufactured bodies: 0")
        vbox_layout1.addWidget(self.body_counter_label)
        vbox_layout1.addWidget(self.production_counter_label)
        vbox_layout1.addWidget(self.finished_bodys_label)

        vbox_layout2 = QVBoxLayout()
        self.label_tmp = self.create_label("No quantity selected")
        vbox_layout2.addWidget(self.label_tmp)
        chose_value_button = AnimatedButton("Chose quantity")
        produce_button = AnimatedButton("Manufacture...")
        vbox_layout2.addWidget(chose_value_button)
        vbox_layout2.addWidget(produce_button)

        hbox_layout1.addLayout(vbox_layout1)
        hbox_layout1.addLayout(vbox_layout2)
        group_box2.setLayout(hbox_layout1)

        layout1.addWidget(group_box2)
        layout1.addWidget(group_box1)
        self.setLayout(layout1)

        # Store button references for signal connection
        self.read_file_button = read_file_button
        self.chose_file_button = chose_file_button

    def create_label(self, label_str: str, max_height: int = 70):
        label = QLabel(label_str)
        label.setStyleSheet(StyleSheet.QLabel.value)
        label.setMaximumHeight(max_height)
        return label
