from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from core.signature_engine import verify_signature, SignatureError


class VerifySignaturePage(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.public_key = None
        self.signature_file = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Verify Signature")
        title.setObjectName("pageTitle")

        info = QLabel(
            "Verify that a file was signed by the private-key owner\n"
            "and that the file was not modified."
        )

        self.file_label = QLabel("No file selected")
        select_file_button = QPushButton("Select Original File")
        select_file_button.clicked.connect(self.select_file)

        self.key_label = QLabel("No public key selected")
        select_key_button = QPushButton("Select Public Key")
        select_key_button.clicked.connect(self.select_public_key)

        self.signature_label = QLabel("No signature selected")
        select_signature_button = QPushButton("Select Signature File")
        select_signature_button.clicked.connect(self.select_signature)

        verify_button = QPushButton("Verify Signature")
        verify_button.clicked.connect(self.verify_selected_signature)

        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(info)
        layout.addSpacing(20)
        layout.addWidget(self.file_label)
        layout.addWidget(select_file_button)
        layout.addWidget(self.key_label)
        layout.addWidget(select_key_button)
        layout.addWidget(self.signature_label)
        layout.addWidget(select_signature_button)
        layout.addWidget(verify_button)
        layout.addStretch()

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select original file")
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path)

    def select_public_key(self):
        key_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select public key",
            "",
            "PEM Files (*.pem)",
        )

        if key_path:
            self.public_key = key_path
            self.key_label.setText(key_path)

    def select_signature(self):
        sig_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select signature file",
            "",
            "Signature Files (*.sig)",
        )

        if sig_path:
            self.signature_file = sig_path
            self.signature_label.setText(sig_path)

    def verify_selected_signature(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select the original file.")
            return

        if not self.public_key:
            QMessageBox.warning(self, "Error", "Please select the public key.")
            return

        if not self.signature_file:
            QMessageBox.warning(self, "Error", "Please select the signature file.")
            return

        try:
            valid = verify_signature(
                self.selected_file,
                self.public_key,
                self.signature_file,
            )

            if valid:
                QMessageBox.information(
                    self,
                    "Signature Valid",
                    "Signature is valid. File is authentic and unchanged.",
                )
            else:
                QMessageBox.critical(
                    self,
                    "Signature Invalid",
                    "Signature is invalid. File may be modified or signed by another key.",
                )

        except SignatureError as e:
            QMessageBox.critical(self, "Signature Error", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))