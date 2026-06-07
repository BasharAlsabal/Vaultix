from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QMessageBox,
)

from core.crypto_engine import decrypt_folder, CryptoError


class DecryptFolderPage(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Decrypt Folder")
        title.setObjectName("pageTitle")

        self.file_label = QLabel("No encrypted folder selected")

        select_button = QPushButton("Select .vaultix Folder Package")
        select_button.clicked.connect(self.select_file)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)

        decrypt_button = QPushButton("Decrypt Folder")
        decrypt_button.clicked.connect(self.decrypt_selected_folder)

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
            "Select encrypted folder package",
            "",
            "Vaultix Files (*.vaultix)",
        )

        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path)

    def decrypt_selected_folder(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a .vaultix file first.")
            return

        password = self.password_input.text()

        output_folder = QFileDialog.getExistingDirectory(
            self,
            "Select folder to extract decrypted folder",
        )

        if not output_folder:
            return

        try:
            decrypt_folder(self.selected_file, output_folder, password)
            QMessageBox.information(
                self,
                "Success",
                f"Folder decrypted successfully into:\n{output_folder}",
            )
        except CryptoError as e:
            QMessageBox.critical(self, "Decryption Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))