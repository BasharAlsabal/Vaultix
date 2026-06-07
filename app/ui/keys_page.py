from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QMessageBox,
)

from core.key_engine import generate_rsa_key_pair, KeyEngineError


class KeysPage(QWidget):
    def __init__(self):
        super().__init__()

        self.output_folder = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Generate RSA-4096 Keys")
        title.setObjectName("pageTitle")

        info = QLabel(
            "Generate a public/private key pair for secure sharing.\n\n"
            "Public key: share with others.\n"
            "Private key: keep secret and protected."
        )

        self.folder_label = QLabel("No output folder selected")

        select_button = QPushButton("Select Output Folder")
        select_button.clicked.connect(self.select_folder)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Private key password - minimum 8 characters")
        self.password_input.setEchoMode(QLineEdit.Password)

        generate_button = QPushButton("Generate Key Pair")
        generate_button.clicked.connect(self.generate_keys)

        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(info)
        layout.addSpacing(20)
        layout.addWidget(self.folder_label)
        layout.addWidget(select_button)
        layout.addWidget(self.password_input)
        layout.addWidget(generate_button)
        layout.addStretch()

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select folder to save keys",
        )

        if folder:
            self.output_folder = folder
            self.folder_label.setText(folder)

    def generate_keys(self):
        if not self.output_folder:
            QMessageBox.warning(self, "Error", "Please select an output folder first.")
            return

        password = self.password_input.text()

        try:
            private_key_path, public_key_path = generate_rsa_key_pair(
                self.output_folder,
                password,
            )

            QMessageBox.information(
                self,
                "Keys Generated",
                f"Private key:\n{private_key_path}\n\n"
                f"Public key:\n{public_key_path}",
            )

        except KeyEngineError as e:
            QMessageBox.critical(self, "Key Error", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))