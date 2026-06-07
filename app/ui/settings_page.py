from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Settings")
        title.setObjectName("pageTitle")

        info = QLabel(
            "Vaultix — Offline Secure Sharing & Encryption Suite\n\n"
            "Version: 1.0.0\n"
            "Mode: Offline\n"
            "Encryption: AES-256-GCM\n"
            "Key Sharing: RSA-4096 + AES Hybrid\n"
            "Integrity: SHA-256\n\n"
            "© 2026 Bashar Alsabal. All rights reserved."
        )

        info.setAlignment(Qt.AlignTop)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(info)
        layout.addStretch()

        self.setLayout(layout)