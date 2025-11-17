from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog
import os

class FileDialog(QWidget):
    def __init__(self, label: QLabel):
        super().__init__()
        self.label = label
        self.selected_file_path = ""

    def show_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_path, _ = QFileDialog.getOpenFileName(
            None, "Otwórz plik JSON", "",
            "JSON Files (*.json);;All Files (*)",
            options=options
        )

        if not file_path:
            return ""

        if file_path.endswith(".json"):
            self.selected_file_path = file_path
            self.label.setText(f"Wybrano plik: {os.path.basename(file_path)}")
            return file_path

        self.selected_file_path = ""
        self.label.setText(
            f"❌ Zły format pliku! Oczekiwany: .json\n\nWybrano:\n{file_path}"
        )
        return ""


    def get_file_path(self):
        """Return last successfully selected file path."""
        return self.selected_file_path