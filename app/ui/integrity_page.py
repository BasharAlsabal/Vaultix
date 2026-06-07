from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QLineEdit,
    QMessageBox,
)

from core.integrity_engine import (
    calculate_sha256,
    verify_sha256,
    IntegrityError,
)


class IntegrityPage(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("SHA-256 Integrity Verification")
        title.setObjectName("pageTitle")

        self.file_label = QLabel("No file selected")

        select_button = QPushButton("Select File")
        select_button.clicked.connect(self.select_file)

        generate_button = QPushButton("Generate SHA-256 Hash")
        generate_button.clicked.connect(self.generate_hash)

        self.hash_output = QTextEdit()
        self.hash_output.setReadOnly(True)
        self.hash_output.setPlaceholderText("Generated SHA-256 hash will appear here...")

        self.expected_hash_input = QLineEdit()
        self.expected_hash_input.setPlaceholderText("Paste expected SHA-256 hash here")

        verify_button = QPushButton("Verify File Integrity")
        verify_button.clicked.connect(self.verify_hash)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.file_label)
        layout.addWidget(select_button)
        layout.addWidget(generate_button)
        layout.addWidget(self.hash_output)
        layout.addWidget(self.expected_hash_input)
        layout.addWidget(verify_button)
        layout.addStretch()

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select file",
        )

        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path)

    def generate_hash(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a file first.")
            return

        try:
            file_hash = calculate_sha256(self.selected_file)
            self.hash_output.setText(file_hash)

        except IntegrityError as e:
            QMessageBox.critical(self, "Integrity Error", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))

    def verify_hash(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a file first.")
            return

        expected_hash = self.expected_hash_input.text()

        if not expected_hash:
            QMessageBox.warning(self, "Error", "Please paste expected SHA-256 hash.")
            return

        try:
            is_valid = verify_sha256(self.selected_file, expected_hash)

            if is_valid:
                QMessageBox.information(
                    self,
                    "Integrity Verified",
                    "File is original. SHA-256 hash matches.",
                )
            else:
                QMessageBox.critical(
                    self,
                    "Integrity Failed",
                    "File was modified or the hash does not match.",
                )

        except IntegrityError as e:
            QMessageBox.critical(self, "Integrity Error", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))