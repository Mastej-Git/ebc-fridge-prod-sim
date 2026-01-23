from PyQt5.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QFrame,
    QVBoxLayout,
    QMessageBox,
    QFileDialog
)
from qt_classes.ControlTab import ControlTab
from qt_classes.LoadedElementsTab import LoadedElementsTab
from qt_classes.LoggerTab import LoggerTab
from qt_classes.GanttChart import GanttChart
from StyleSheet import StyleSheet
from elements.FileDialog import FileDialog
from utils.json_parser import parse_bodys_json
import os
from threads.ListenerThread import Listener
from threads.WorkerThread import WorkerThread


class GUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Tab Example")
        self.setGeometry(100, 100, 1200, 600)

        self.available_tr = []
        self.set_for_prod = []
        self.fridge_prod_params = {
            'loaded': 0,
            'in_prod': 0,
            'finished': 0,
        }

        central_widget = QFrame()
        central_widget.setStyleSheet(StyleSheet.CentralWidget.value)
        layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        self.tabs.tabBar().setExpanding(True)
        self.tabs.setStyleSheet(StyleSheet.Tab.value)

        self.control_tab = ControlTab()
        self.loaded_elements_tab = LoadedElementsTab()
        self.logger_tab = LoggerTab()

        self.tabs.addTab(self.control_tab, "Control Tab")
        self.tabs.addTab(self.loaded_elements_tab, "Loaded Elements")
        self.tabs.addTab(QFrame(), "Gantt tab")
        self.tabs.addTab(self.logger_tab, "Logger")

        worker_th = WorkerThread(self.available_tr, self.logger_tab, self.fridge_prod_params, self.control_tab, interval=0.5)
        listener_th = Listener(self.available_tr, self.set_for_prod, interval=0.5)
        worker_th.start()
        listener_th.start()

        layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

        self.selected_json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'example.json')
        self._bodies_list = []
        self._manufactured_fridges = []

        self.file_dialog = FileDialog(self.control_tab.config_label)
        self.control_tab.produce_button.clicked.connect(self.pb_manufacture)

        self.connect_signals()

        self.setup_gantt_tab()

        self.update_config_label()

    def connect_signals(self):
        self.control_tab.chose_file_button.clicked.connect(self.pb_chose_file)
        self.control_tab.read_file_button.clicked.connect(self.pb_read_json)

        self.loaded_elements_tab.bodies_list.currentItemChanged.connect(self.on_body_selected)
        self.loaded_elements_tab.product_button.clicked.connect(self.pb_product_fridge)
        self.loaded_elements_tab.remove_button.clicked.connect(self.pb_remove_fridge)

        self.logger_tab.clear_button.clicked.connect(self.pb_clear_logger)

    def setup_gantt_tab(self):
        gantt_tab = self.tabs.widget(2)
        layout = QVBoxLayout()
        gantt_tab.setLayout(layout)

        example_tasks = [
            {"task": "Design", "start": 0, "end": 0},
        ]
        self.gantt_widget = GanttChart(example_tasks)
        layout.addWidget(self.gantt_widget)

    def update_config_label(self):
        try:
            self.control_tab.config_label.setText(os.path.basename(self.selected_json_path))
            self.control_tab.config_label.setToolTip(self.selected_json_path)
        except Exception:
            pass

    def pb_chose_file(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(
            self,
            "Choose JSON file",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options
        )
        if fname:
            self.selected_json_path = fname
            self.update_config_label()

    def pb_read_json(self):
        if not self.selected_json_path:
            QMessageBox.warning(self, "No file chosen", "Please choose a JSON file first.")
            return

        try:
            new_data = parse_bodys_json(self.selected_json_path)
            if new_data is None:
                raise ValueError("Parsed data is empty or invalid.")
            self._normalize_bodies(new_data)
            self.loaded_elements_tab.populate_list(self._bodies_list, self.format_body_details)
            self.fridge_prod_params['loaded'] = len(self._bodies_list)
            self.control_tab.body_counter_label.setText(f"Loaded fridges: {self.fridge_prod_params['loaded']}")
            self.add_log_entry(f"LOADED: {len(self._bodies_list)} fridges loaded from {os.path.basename(self.selected_json_path)}")
            # self.tabs.setCurrentWidget(self.loaded_elements_tab)
        except Exception as e:
            QMessageBox.critical(self, "Load error", f"Failed to load JSON:\n{e}")

    def populate_bodies_list(self):
        self.loaded_elements_tab.populate_list(self._bodies_list, self.format_body_details)

    def _normalize_bodies(self, data):
        if isinstance(data, list):
            self._bodies_list = data
        else:
            self._bodies_list = [data] if data else []
        # print(f"Loaded {len(self._bodies_list)} fridges")

    def on_body_selected(self, current, previous):
        if current is None:
            return
        index = self.loaded_elements_tab.bodies_list.row(current)
        if 0 <= index < len(self._bodies_list):
            detail_text = self.format_body_details(self._bodies_list[index], index + 1)
            self.loaded_elements_tab.update_detail_text(detail_text)

    def format_body_details(self, body_item, body_num):
        output = []
        output.append(f"{'='*70}")
        output.append(f"ID: {body_item.body_id} - Fridge Body Components")
        output.append(f"{'='*70}")

        output.append("▸ Cover:")
        output.append(f"  ▪  Material: {body_item.cover.material}")
        output.append(f"  ▪  Color: {body_item.cover.color}")

        output.append("▸ Doors:")
        output.append(f"  ▪  Material: {body_item.doors.material}")
        output.append(f"  ▪  Machine: {body_item.doors.machine}")
        output.append(f"  ▪  Front Panel: {body_item.doors.front_panel}")

        output.append("▸ Shelves:")
        output.append(f"  ▪  Number: {body_item.shelves.quantity}")
        output.append(f"  ▪  Adjustable Height: {body_item.shelves.adjustable}")
        output.append(f"  ▪  Material: {body_item.shelves.material}")

        output.append("▸ Cooling System:")
        output.append(f"  ▪  Type: {body_item.cooling_system.type}")
        output.append(f"  ▪  Energy Class: {body_item.cooling_system.energy_class}")

        output.append("▸ Lighting:")
        output.append(f"  ▪  Internal Lights: {body_item.lights.type}")
        output.append(f"  ▪  Automatic Light On: {body_item.lights.automatic}")

        output.append(f"\n{'='*70}\n")
        return "\n".join(output)

    def add_log_entry(self, message: str):
        self.logger_tab.add_entry(message)

    def pb_clear_logger(self):
        self.logger_tab.clear()

    def pb_product_fridge(self):
        current_item = self.loaded_elements_tab.bodies_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "No selection", "Please select a fridge to mark as product.")
            return
        index = self.loaded_elements_tab.bodies_list.row(current_item)
        fridge = self._bodies_list[index]
        fridge_id = fridge.body_id
        self.add_log_entry(f"PRODUCTION: Fridge ID {fridge_id} is now in production.")
        try:
            if hasattr(self, 'gantt_widget') and self.gantt_widget is not None:
                self.gantt_widget.add_fridge(fridge, fridge_id)
        except Exception as e:
            print(f"Gantt error: {e}")

        self.set_for_prod.append(fridge)
        QMessageBox.information(self, "For production", f"Fridge ID {fridge_id} is now in production.")

    def pb_remove_fridge(self):
        current_item = self.loaded_elements_tab.bodies_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "No selection", "Please select a fridge to remove.")
            return
        index = self.loaded_elements_tab.bodies_list.row(current_item)
        fridge_id = self._bodies_list[index].body_id
        reply = QMessageBox.question(self, "Confirm Remove", f"Remove fridge ID {fridge_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self._bodies_list[index]
            self.add_log_entry(f"REMOVED: Fridge ID {fridge_id} has been removed from production.")
            self.populate_bodies_list()
            if self._bodies_list:
                self.loaded_elements_tab.update_detail_text(self.format_body_details(self._bodies_list[0], 1))
            else:
                self.loaded_elements_tab.update_detail_text("No bodies loaded. Use the Control Tab to load a JSON file.")

    def pb_manufacture(self):
        if self.control_tab.selected_quantity != 0 and len(self._bodies_list) >= self.control_tab.selected_quantity:
            for i in range(self.control_tab.selected_quantity):
                fridge = self._bodies_list[i]
                self.set_for_prod.append(fridge)
                try:
                    if hasattr(self, 'gantt_widget') and self.gantt_widget is not None:
                        self.gantt_widget.add_fridge(fridge, fridge.body_id)
                except Exception as e:
                    print(f"Gantt error: {e}")
    