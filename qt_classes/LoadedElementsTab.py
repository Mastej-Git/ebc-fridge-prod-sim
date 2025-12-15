from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QTextEdit,
    QListWidget,
    QListWidgetItem,
    QSplitter
)
from PyQt5.QtCore import Qt
from qt_classes.AnimatedButton import AnimatedButton


class LoadedElementsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.bodies_list = None
        self.body_detail_text = None
        self.init_ui()

    def init_ui(self):
        layout2 = QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        # Bodies list
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

        # Detail panel
        detail_panel = QWidget()
        detail_layout = QVBoxLayout(detail_panel)

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
        self.body_detail_text.setText("No bodies loaded. Use the Control Tab to load a JSON file.")
        detail_layout.addWidget(self.body_detail_text)

        # Button panel
        button_panel = QFrame()
        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(5, 5, 5, 5)
        button_layout.setSpacing(5)

        self.product_button = AnimatedButton("For production")
        self.remove_button = AnimatedButton("Remove")

        button_layout.addWidget(self.product_button)
        button_layout.addWidget(self.remove_button)

        detail_layout.addWidget(button_panel)

        splitter.addWidget(self.bodies_list)
        splitter.addWidget(detail_panel)
        splitter.setSizes([200, 600])

        layout2.addWidget(splitter)
        self.setLayout(layout2)

    def populate_list(self, bodies_list, format_func):
        """Populate the list with bodies."""
        self.bodies_list.clear()
        for idx in range(len(bodies_list)):
            fridge_id = bodies_list[idx].get('id', idx + 1)
            item = QListWidgetItem(f"body_{fridge_id}")
            self.bodies_list.addItem(item)
        if bodies_list:
            self.bodies_list.setCurrentRow(0)
            self.body_detail_text.setText(format_func(bodies_list[0], 1))
        else:
            self.body_detail_text.setText("No bodies loaded")

    def update_detail_text(self, text):
        """Update the detail text display."""
        self.body_detail_text.setText(text)