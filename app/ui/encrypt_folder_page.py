from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QMessageBox,
)

from core.crypto_engine import encrypt_folder, CryptoError


class EncryptFolderPage(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_folder = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Encrypt Folder")
        title.setObjectName("pageTitle")

        self.folder_label = QLabel("No folder selected")

        select_button = QPushButton("Select Folder")
        select_button.clicked.connect(self.select_folder)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password - minimum 8 characters")
        self.password_input.setEchoMode(QLineEdit.Password)

        encrypt_button = QPushButton("Encrypt Folder")
        encrypt_button.clicked.connect(self.encrypt_selected_folder)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.folder_label)
        layout.addWidget(select_button)
        layout.addWidget(self.password_input)
        layout.addWidget(encrypt_button)
        layout.addStretch()

        self.setLayout(layout)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select folder to encrypt",
        )

        if folder_path:
            self.selected_folder = folder_path
            self.folder_label.setText(folder_path)

    def encrypt_selected_folder(self):
        if not self.selected_folder:
            QMessageBox.warning(self, "Error", "Please select a folder first.")
            return

        password = self.password_input.text()

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save encrypted folder",
            self.selected_folder + ".vaultix",
            "Vaultix Files (*.vaultix)",
        )

        if not output_path:
            return

        try:
            encrypt_folder(self.selected_folder, output_path, password)
            QMessageBox.information(
                self,
                "Success",
                f"Folder encrypted successfully:\n{output_path}",
            )
        except CryptoError as e:
            QMessageBox.critical(self, "Encryption Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))