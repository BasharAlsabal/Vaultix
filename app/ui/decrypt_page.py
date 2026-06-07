from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QMessageBox,
)

from core.crypto_engine import decrypt_file, CryptoError
from database.db_manager import add_history


class DecryptPage(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Decrypt File")
        title.setObjectName("pageTitle")

        self.file_label = QLabel("No encrypted file selected")

        select_button = QPushButton("Select .vaultix File")
        select_button.clicked.connect(self.select_file)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)

        decrypt_button = QPushButton("Decrypt File")
        decrypt_button.clicked.connect(self.decrypt_selected_file)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.file_label)
        layout.addWidget(select_button)
        layout.addWidget(self.password_input)
        layout.addWidget(decrypt_button)
        layout.addStretch()

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select encrypted file",
            "",
            "Vaultix Files (*.vaultix)",
        )

        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path)

    def decrypt_selected_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select an encrypted file first.")
            return

        password = self.password_input.text()

        output_folder = QFileDialog.getExistingDirectory(
            self,
            "Select folder to save decrypted file",
        )

        if not output_folder:
            return

        try:
            output_path = decrypt_file(self.selected_file, output_folder, password)
            add_history("Decrypt File", self.selected_file, "Success")
            QMessageBox.information(
                self,
                "Success",
                f"File decrypted successfully:\n{output_path}",
            )
        except CryptoError as e:
            add_history("Decrypt File", self.selected_file, "Failed")
            QMessageBox.critical(self, "Decryption Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))