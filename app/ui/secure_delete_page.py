from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QSpinBox,
)

from core.shredder_engine import secure_delete, ShredderError
from database.db_manager import add_history


class SecureDeletePage(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Secure Delete")
        title.setObjectName("pageTitle")

        info = QLabel(
            "Permanently delete a file by overwriting it before removal.\n"
            "Use carefully. This action cannot be undone."
        )

        self.file_label = QLabel("No file selected")

        select_button = QPushButton("Select File")
        select_button.clicked.connect(self.select_file)

        self.passes_input = QSpinBox()
        self.passes_input.setMinimum(1)
        self.passes_input.setMaximum(10)
        self.passes_input.setValue(3)

        delete_button = QPushButton("Secure Delete File")
        delete_button.clicked.connect(self.delete_file)

        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(info)
        layout.addSpacing(20)
        layout.addWidget(self.file_label)
        layout.addWidget(select_button)
        layout.addWidget(QLabel("Overwrite passes:"))
        layout.addWidget(self.passes_input)
        layout.addWidget(delete_button)
        layout.addStretch()

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select file to securely delete",
        )

        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path)

    def delete_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a file first.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Secure Delete",
            "This will permanently overwrite and delete the selected file.\n\n"
            "This action cannot be undone.\n\n"
            "Are you sure?",
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            secure_delete(
                self.selected_file,
                self.passes_input.value(),
            )

            add_history("Secure Delete", self.selected_file, "Success")

            QMessageBox.information(
                self,
                "Deleted",
                "File was securely deleted.",
            )

            self.file_label.setText("No file selected")
            self.selected_file = None

        except ShredderError as e:
            add_history("Secure Delete", self.selected_file, "Failed")
            QMessageBox.critical(self, "Secure Delete Error", str(e))

        except Exception as e:
            add_history("Secure Delete", self.selected_file, "Failed")
            QMessageBox.critical(self, "Unexpected Error", str(e))