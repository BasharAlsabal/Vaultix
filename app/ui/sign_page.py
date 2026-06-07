from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QMessageBox,
)

from core.signature_engine import sign_file, SignatureError


class SignPage(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.private_key = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Sign File")
        title.setObjectName("pageTitle")

        info = QLabel(
            "Create a digital signature using your private key.\n"
            "The receiver can verify it using your public key."
        )

        self.file_label = QLabel("No file selected")
        select_file_button = QPushButton("Select File")
        select_file_button.clicked.connect(self.select_file)

        self.key_label = QLabel("No private key selected")
        select_key_button = QPushButton("Select Private Key")
        select_key_button.clicked.connect(self.select_private_key)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Private key password")
        self.password_input.setEchoMode(QLineEdit.Password)

        sign_button = QPushButton("Sign File")
        sign_button.clicked.connect(self.sign_selected_file)

        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(info)
        layout.addSpacing(20)
        layout.addWidget(self.file_label)
        layout.addWidget(select_file_button)
        layout.addWidget(self.key_label)
        layout.addWidget(select_key_button)
        layout.addWidget(self.password_input)
        layout.addWidget(sign_button)
        layout.addStretch()

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file to sign")
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path)

    def select_private_key(self):
        key_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select private key",
            "",
            "PEM Files (*.pem)",
        )

        if key_path:
            self.private_key = key_path
            self.key_label.setText(key_path)

    def sign_selected_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a file first.")
            return

        if not self.private_key:
            QMessageBox.warning(self, "Error", "Please select your private key.")
            return

        password = self.password_input.text()

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save signature file",
            self.selected_file + ".sig",
            "Signature Files (*.sig)",
        )

        if not output_path:
            return

        try:
            sign_file(
                self.selected_file,
                self.private_key,
                password,
                output_path,
            )

            QMessageBox.information(
                self,
                "Signature Created",
                f"Signature saved successfully:\n{output_path}",
            )

        except SignatureError as e:
            QMessageBox.critical(self, "Signature Error", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))