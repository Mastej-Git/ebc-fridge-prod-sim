from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QTextEdit
)
from qt_classes.AnimatedButton import AnimatedButton
from datetime import datetime
from StyleSheet import StyleSheet


class LoggerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.logger_text = None
        self.init_ui()

    def init_ui(self):
        layout4 = QVBoxLayout()

        logger_title = QLabel("Production Logger")
        logger_title.setStyleSheet(StyleSheet.QLoggerTitle.value)
        layout4.addWidget(logger_title)

        self.logger_text = QTextEdit()
        self.logger_text.setReadOnly(True)
        self.logger_text.setStyleSheet(StyleSheet.QLoggerText.value)
        self.logger_text.setText("Production Logger - Ready\n" + "="*70 + "\n")
        layout4.addWidget(self.logger_text)

        control_panel = QFrame()
        control_layout = QHBoxLayout(control_panel)
        control_layout.setContentsMargins(5, 5, 5, 5)
        control_layout.setSpacing(5)

        self.clear_button = AnimatedButton("Clear Log")
        control_layout.addStretch()
        control_layout.addWidget(self.clear_button)

        layout4.addWidget(control_panel)
        self.setLayout(layout4)

    def add_entry(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.logger_text.append(log_entry)
        self.logger_text.verticalScrollBar().setValue(
            self.logger_text.verticalScrollBar().maximum()
        )

    def clear(self):
        self.logger_text.setText("Production Logger - Cleared\n" + "="*70 + "\n")
        