from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QPushButton,
)
from PySide6.QtCore import Qt

from database.db_manager import get_dashboard_stats


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.cards = {}
        self.setup_ui()
        self.refresh_stats()

    def create_card(self, key: str, title: str, value: str, description: str):
        card = QFrame()
        card.setObjectName("dashboardCard")

        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        value_label = QLabel(value)
        value_label.setObjectName("cardValue")

        desc_label = QLabel(description)
        desc_label.setObjectName("cardDescription")
        desc_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(desc_label)

        self.cards[key] = value_label

        return card

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        title = QLabel("Vaultix Dashboard")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Offline Secure Sharing & Encryption Suite\n"
            "Protect, encrypt, sign, verify, hide, and securely share sensitive data."
        )
        subtitle.setObjectName("dashboardSubtitle")

        refresh_button = QPushButton("Refresh Dashboard")
        refresh_button.clicked.connect(self.refresh_stats)

        row1 = QHBoxLayout()
        row1.addWidget(self.create_card(
            "total_operations",
            "Total Operations",
            "0",
            "All logged Vaultix security operations."
        ))
        row1.addWidget(self.create_card(
            "encrypted_files",
            "Files Encrypted",
            "0",
            "Password-based AES-256-GCM encryption operations."
        ))
        row1.addWidget(self.create_card(
            "decrypted_files",
            "Files Decrypted",
            "0",
            "Successful decryption operations."
        ))

        row2 = QHBoxLayout()
        row2.addWidget(self.create_card(
            "secure_deletes",
            "Secure Deletes",
            "0",
            "Files permanently shredded using overwrite passes."
        ))
        row2.addWidget(self.create_card(
            "crypto",
            "Crypto Engine",
            "AES/RSA",
            "AES-256-GCM, RSA-4096, SHA-256, and signatures."
        ))
        row2.addWidget(self.create_card(
            "mode",
            "Mode",
            "Offline",
            "Vaultix works locally without internet dependency."
        ))

        footer = QLabel("© 2026 Bashar Alsabal. All rights reserved.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setObjectName("footerText")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(refresh_button)
        main_layout.addLayout(row1)
        main_layout.addLayout(row2)
        main_layout.addStretch()
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def refresh_stats(self):
        stats = get_dashboard_stats()

        self.cards["total_operations"].setText(str(stats["total_operations"]))
        self.cards["encrypted_files"].setText(str(stats["encrypted_files"]))
        self.cards["decrypted_files"].setText(str(stats["decrypted_files"]))
        self.cards["secure_deletes"].setText(str(stats["secure_deletes"]))