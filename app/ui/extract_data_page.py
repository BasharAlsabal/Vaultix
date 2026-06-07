from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from core.stego_engine import extract_file_from_png, StegoError


class ExtractDataPage(QWidget):
    def __init__(self):
        super().__init__()

        self.stego_image = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Extract Hidden Data")
        title.setObjectName("pageTitle")

        self.image_label = QLabel("No stego image selected")

        btn_image = QPushButton("Select Stego PNG")
        btn_extract = QPushButton("Extract File")

        btn_image.clicked.connect(self.select_image)
        btn_extract.clicked.connect(self.extract_file)

        layout.addWidget(title)
        layout.addWidget(self.image_label)
        layout.addWidget(btn_image)
        layout.addWidget(btn_extract)
        layout.addStretch()

        self.setLayout(layout)

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PNG",
            "",
            "PNG Files (*.png)"
        )

        if path:
            self.stego_image = path
            self.image_label.setText(path)

    def extract_file(self):
        if not self.stego_image:
            QMessageBox.warning(self, "Error", "Select stego image.")
            return

        output_folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder"
        )

        if not output_folder:
            return

        try:
            output_path = extract_file_from_png(
                self.stego_image,
                output_folder
            )

            QMessageBox.information(
                self,
                "Success",
                f"Extracted:\n{output_path}"
            )

        except StegoError as e:
            QMessageBox.critical(self, "Stego Error", str(e))