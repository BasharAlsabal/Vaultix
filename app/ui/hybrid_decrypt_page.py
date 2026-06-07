from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QMessageBox,
)

from core.hybrid_engine import decrypt_from_sender, HybridError


class HybridDecryptPage(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_package = None
        self.private_key = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Decrypt Secure Sharing Package")
        title.setObjectName("pageTitle")

        info = QLabel(
            "Decrypt a .vshare package using your private key.\n"
            "This is used when someone encrypted a file with your public key."
        )

        self.package_label = QLabel("No .vshare package selected")
        select_package_button = QPushButton("Select .vshare Package")
        select_package_button.clicked.connect(self.select_package)

        self.key_label = QLabel("No private key selected")
        select_key_button = QPushButton("Select Your Private Key")
        select_key_button.clicked.connect(self.select_private_key)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Private key password")
        self.password_input.setEchoMode(QLineEdit.Password)

        decrypt_button = QPushButton("Decrypt Package")
        decrypt_button.clicked.connect(self.decrypt_package)

        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(info)
        layout.addSpacing(20)
        layout.addWidget(self.package_label)
        layout.addWidget(select_package_button)
        layout.addWidget(self.key_label)
        layout.addWidget(select_key_button)
        layout.addWidget(self.password_input)
        layout.addWidget(decrypt_button)
        layout.addStretch()

        self.setLayout(layout)

    def select_package(self):
        package_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select .vshare package",
            "",
            "Vaultix Share Files (*.vshare)",
        )

        if package_path:
            self.selected_package = package_path
            self.package_label.setText(package_path)

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

    def decrypt_package(self):
        if not self.selected_package:
            QMessageBox.warning(self, "Error", "Please select a .vshare package.")
            return

        if not self.private_key:
            QMessageBox.warning(self, "Error", "Please select your private key.")
            return

        password = self.password_input.text()

        output_folder = QFileDialog.getExistingDirectory(
            self,
            "Select output folder",
        )

        if not output_folder:
            return

        try:
            output_path = decrypt_from_sender(
                self.selected_package,
                self.private_key,
                password,
                output_folder,
            )

            QMessageBox.information(
                self,
                "Package Decrypted",
                f"File decrypted successfully:\n{output_path}",
            )

        except HybridError as e:
            QMessageBox.critical(self, "Hybrid Decryption Error", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))