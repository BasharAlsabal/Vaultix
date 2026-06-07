from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from core.stego_engine import hide_file_in_png, StegoError


class HideDataPage(QWidget):
    def __init__(self):
        super().__init__()

        self.cover_image = None
        self.secret_file = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Hide Data Inside PNG")
        title.setObjectName("pageTitle")

        self.image_label = QLabel("No PNG image selected")
        self.file_label = QLabel("No secret file selected")

        btn_image = QPushButton("Select PNG Image")
        btn_file = QPushButton("Select Secret File")
        btn_hide = QPushButton("Hide File")

        btn_image.clicked.connect(self.select_image)
        btn_file.clicked.connect(self.select_file)
        btn_hide.clicked.connect(self.hide_data)

        layout.addWidget(title)
        layout.addWidget(self.image_label)
        layout.addWidget(btn_image)
        layout.addWidget(self.file_label)
        layout.addWidget(btn_file)
        layout.addWidget(btn_hide)
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
            self.cover_image = path
            self.image_label.setText(path)

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Secret File")

        if path:
            self.secret_file = path
            self.file_label.setText(path)

    def hide_data(self):
        if not self.cover_image:
            QMessageBox.warning(self, "Error", "Select PNG image.")
            return

        if not self.secret_file:
            QMessageBox.warning(self, "Error", "Select secret file.")
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Stego Image",
            "vaultix_hidden.png",
            "PNG Files (*.png)"
        )

        if not output_path:
            return

        try:
            hide_file_in_png(
                self.cover_image,
                self.secret_file,
                output_path
            )

            QMessageBox.information(
                self,
                "Success",
                f"Hidden data saved:\n{output_path}"
            )

        except StegoError as e:
            QMessageBox.critical(self, "Stego Error", str(e))