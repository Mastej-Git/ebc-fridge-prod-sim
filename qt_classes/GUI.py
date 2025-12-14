from PyQt5.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QFrame,
    QTextEdit,
    QListWidget,
    QListWidgetItem,
    QSplitter
)
from PyQt5.QtCore import Qt
from qt_classes.AnimatedButton import AnimatedButton
from qt_classes.GanttChart import GanttChart
from StyleSheet import StyleSheet
from elements.FileDialog import FileDialog
from utils.json_parser import parse_bodys_json
import os

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
        self.tabs.addTab(self.tab1, "Control Tab")
        self.tabs.addTab(self.tab2, "Loaded Elements")
        self.tabs.addTab(self.tab3, "Gantt tab")

        self.create_tab_content()
        layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

    def create_tab_content(self):
        sub_tab_widget = QTabWidget()
        sub_tab_widget.setTabPosition(QTabWidget.West)
        sub_tab_widget.setStyleSheet(StyleSheet.SubTab.value)

        self.create_dial_tab()
        self.create_loaded_elements_tab()

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

        group_box1 = QGroupBox("Load configuration")
        group_box1.setFixedHeight(200)

        label = QLabel("No file selected")

        hbox_layout = QHBoxLayout()
        vbox_layout = QVBoxLayout()

        read_file_button = AnimatedButton("Load")
        # read_file_button.clicked.connect(self.pb_read_json)

        self.file_dialog = FileDialog(label)

        chose_file_button = AnimatedButton("Chose a file")
        # chose_file_button.clicked.connect(self.pb_chose_file)

        vbox_layout.addWidget(chose_file_button)
        vbox_layout.addWidget(read_file_button)

        hbox_layout.addWidget(label)
        hbox_layout.addLayout(vbox_layout)

        group_box2 = QGroupBox("Control panel")
        group_box2.setFixedHeight(600)


        hbox_layout1 = QHBoxLayout()

        vbox_layout1 = QVBoxLayout()
        body_counter_label = self.create_label("Loaded bodies: 0")
        production_counter_label = self.create_label("Bodies in production: 0")
        finished_bodys_label = self.create_label("Manufactured bodies: 0")
        vbox_layout1.addWidget(body_counter_label)
        vbox_layout1.addWidget(production_counter_label)
        vbox_layout1.addWidget(finished_bodys_label)

        vbox_layout2 = QVBoxLayout()
        self.label_tmp = self.create_label("No quantity selected")
        vbox_layout2.addWidget(self.label_tmp)
        chose_value_button = AnimatedButton("Chose quantity")
        # chose_value_button.clicked.connect(self.pb_input_dialog)
        vbox_layout2.addWidget(chose_value_button)
        produce_button = AnimatedButton("Manufacture...")
        # produce_button.clicked.connect(self.pb_produce)
        vbox_layout2.addWidget(produce_button)

        hbox_layout1.addLayout(vbox_layout1)
        hbox_layout1.addLayout(vbox_layout2)

        group_box2.setLayout(hbox_layout1)
        group_box1.setLayout(hbox_layout)

        layout1.addWidget(group_box2)
        layout1.addWidget(group_box1)
        self.tab1.setLayout(layout1)

    def create_loaded_elements_tab(self):
        """Create the Loaded Elements tab with clickable list and detail view."""
        layout2 = QVBoxLayout()

        json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bodys.json') # Right now just load the hard-coded file
        self.bodies_data = parse_bodys_json(json_path)

        splitter = QSplitter(Qt.Horizontal)

        self.bodies_list = QListWidget()
        self.bodies_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: #00ffff;
                border: 1px solid #404040;
                font-size: 12pt;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #404040;
            }
            QListWidget::item:selected {
                background-color: #404040;
                color: #00ff00;
            }
            QListWidget::item:hover {
                background-color: #353535;
            }
        """)

        # Populate the list with body items
        for idx in range(len(self.bodies_data)):
            item = QListWidgetItem(f"body_{idx + 1}")
            self.bodies_list.addItem(item)

        self.bodies_list.currentItemChanged.connect(self.on_body_selected)

        self.body_detail_text = QTextEdit()
        self.body_detail_text.setReadOnly(True)
        self.body_detail_text.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #00ffff;
                border: 1px solid #404040;
                padding: 10px;
                font-family: monospace;
                font-size: 11pt;
            }
        """)
        self.body_detail_text.setText("Select a body from the list to view details")

        splitter.addWidget(self.bodies_list)
        splitter.addWidget(self.body_detail_text)
        splitter.setSizes([200, 600])

        layout2.addWidget(splitter)
        self.tab2.setLayout(layout2)

    # VIBE CODED SHIT FOR LOADING CAR DATA AT FIRST
    def on_body_selected(self, current, previous):
        """Handle body item selection and display details."""
        if current is None:
            return

        index = self.bodies_list.row(current)

        if 0 <= index < len(self.bodies_data):
            body_data = self.bodies_data[index]

            detail_text = self.format_body_details(body_data, index + 1)
            self.body_detail_text.setText(detail_text)

    def format_body_details(self, body_item, body_num):
        """Format body details for display."""
        output = []
        output.append(f"{'='*60}")
        output.append(f"BODY #{body_num}")
        output.append(f"{'='*60}")

        if 'body' in body_item:
            body = body_item['body']

            # Upper Panel
            if 'upper_panel' in body:
                output.append("\nUpper Panel:")
                output.append(f"  Controllable: {body['upper_panel'].get('is_controllable', 'N/A')}")
                output.append(f"  Type: {body['upper_panel'].get('type', 'N/A')}")

            # Framework
            if 'framework' in body:
                output.append("\nFramework:")
                output.append(f"  Material: {body['framework'].get('material', 'N/A')}")
                output.append(f"  Color: {body['framework'].get('color', 'N/A')}")

            # Middle Panel
            if 'middle_panel' in body:
                output.append("\nMiddle Panel:")
                output.append(f"  Functionality: {body['middle_panel'].get('functionality', 'N/A')}")

            # Lower Panel
            if 'lower_panel' in body:
                output.append("\nLower Panel:")
                output.append(f"  Functionality: {body['lower_panel'].get('functionality', 'N/A')}")
                output.append(f"  Cup Holder: {body['lower_panel'].get('is_cup', 'N/A')}")
                output.append(f"  Color: {body['lower_panel'].get('color', 'N/A')}")

            # Armrest
            if 'armrest' in body:
                output.append("\nArmrest:")
                output.append(f"  Heating: {body['armrest'].get('heating', 'N/A')}")
                output.append(f"  Material: {body['armrest'].get('material', 'N/A')}")
                output.append(f"  Color: {body['armrest'].get('color', 'N/A')}")

            # Cup Holder
            if 'cup_holder' in body:
                output.append("\nCup Holder:")
                output.append(f"  USB Socket: {body['cup_holder'].get('usb_socket', 'N/A')}")
                output.append(f"  Color: {body['cup_holder'].get('color', 'N/A')}")

        return "\n".join(output)

    def create_label(self, label_str: str, maximuxm_height: int = 70) -> QLabel:
        label = QLabel(label_str)
        label.setStyleSheet(StyleSheet.QLabel.value)
        label.setMaximumHeight(maximuxm_height)
        return label
