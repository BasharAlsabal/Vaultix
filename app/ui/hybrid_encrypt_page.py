from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from core.hybrid_engine import encrypt_for_receiver, HybridError


class HybridEncryptPage(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.public_key = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Public-Key Secure Sharing")
        title.setObjectName("pageTitle")

        info = QLabel(
            "Encrypt a file using the receiver's public key.\n"
            "Only the receiver's private key can decrypt it."
        )

        self.file_label = QLabel("No file selected")
        select_file_button = QPushButton("Select File")
        select_file_button.clicked.connect(self.select_file)

        self.key_label = QLabel("No receiver public key selected")
        select_key_button = QPushButton("Select Receiver Public Key")
        select_key_button.clicked.connect(self.select_public_key)

        encrypt_button = QPushButton("Encrypt for Receiver")
        encrypt_button.clicked.connect(self.encrypt_file_for_receiver)

        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(info)
        layout.addSpacing(20)
        layout.addWidget(self.file_label)
        layout.addWidget(select_file_button)
        layout.addWidget(self.key_label)
        layout.addWidget(select_key_button)
        layout.addWidget(encrypt_button)
        layout.addStretch()

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file to encrypt")
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path)

    def select_public_key(self):
        key_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select receiver public key",
            "",
            "PEM Files (*.pem)",
        )

        if key_path:
            self.public_key = key_path
            self.key_label.setText(key_path)

    def encrypt_file_for_receiver(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a file first.")
            return

        if not self.public_key:
            QMessageBox.warning(self, "Error", "Please select receiver public key.")
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save secure sharing package",
            self.selected_file + ".vshare",
            "Vaultix Share Files (*.vshare)",
        )

        if not output_path:
            return

        try:
            encrypt_for_receiver(
                self.selected_file,
                self.public_key,
                output_path,
            )

            QMessageBox.information(
                self,
                "Secure Package Created",
                f"Encrypted package saved:\n{output_path}",
            )

        except HybridError as e:
            QMessageBox.critical(self, "Hybrid Encryption Error", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))