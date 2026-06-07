from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QMessageBox,
)

from core.crypto_engine import encrypt_file, CryptoError
from database.db_manager import add_history


class EncryptPage(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Encrypt File")
        title.setObjectName("pageTitle")

        self.file_label = QLabel("No file selected")

        select_button = QPushButton("Select File")
        select_button.clicked.connect(self.select_file)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password - minimum 8 characters")
        self.password_input.setEchoMode(QLineEdit.Password)

        encrypt_button = QPushButton("Encrypt File")
        encrypt_button.clicked.connect(self.encrypt_selected_file)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.file_label)
        layout.addWidget(select_button)
        layout.addWidget(self.password_input)
        layout.addWidget(encrypt_button)
        layout.addStretch()

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select file to encrypt",
        )

        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path)

    def encrypt_selected_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a file first.")
            return

        password = self.password_input.text()

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save encrypted file",
            self.selected_file + ".vaultix",
            "Vaultix Files (*.vaultix)",
        )

        if not output_path:
            return

        try:
            encrypt_file(self.selected_file, output_path, password)
            add_history("Encrypt File", self.selected_file, "Success")
            QMessageBox.information(
                self,
                "Success",
                f"File encrypted successfully:\n{output_path}",
            )
        except CryptoError as e:
            add_history("Encrypt File", self.selected_file, "Failed")
            QMessageBox.critical(self, "Encryption Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))