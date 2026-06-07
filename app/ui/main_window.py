from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QScrollArea
)

from ui.dashboard_page import DashboardPage
from ui.encrypt_page import EncryptPage
from ui.decrypt_page import DecryptPage
from ui.encrypt_folder_page import EncryptFolderPage
from ui.decrypt_folder_page import DecryptFolderPage
from ui.integrity_page import IntegrityPage
from ui.keys_page import KeysPage
from ui.sign_page import SignPage
from ui.verify_signature_page import VerifySignaturePage
from ui.hybrid_encrypt_page import HybridEncryptPage
from ui.hybrid_decrypt_page import HybridDecryptPage
from ui.hide_data_page import HideDataPage
from ui.extract_data_page import ExtractDataPage
from ui.secure_delete_page import SecureDeletePage
from ui.history_page import HistoryPage
from ui.settings_page import SettingsPage
from PySide6.QtGui import QIcon


class VaultixMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vaultix")
        self.setWindowIcon(QIcon("app/assets/vaultix.ico"))
        self.resize(1250, 760)

        self.nav_buttons = []
        self.setup_ui()
        self.apply_dark_theme()
        self.set_active_button(0)

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar_container = QWidget()
        sidebar_container.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(14, 18, 14, 18)
        sidebar_layout.setSpacing(8)

        logo = QLabel("Vaultix")
        logo.setObjectName("logo")

        subtitle = QLabel("Secure Offline Suite")
        subtitle.setObjectName("sidebarSubtitle")

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(subtitle)
        sidebar_layout.addSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setSpacing(7)
        nav_layout.setContentsMargins(0, 0, 0, 0)

        self.pages = QStackedWidget()

        page_data = [
            ("Dashboard", DashboardPage()),
            ("Encrypt File", EncryptPage()),
            ("Decrypt File", DecryptPage()),
            ("Encrypt Folder", EncryptFolderPage()),
            ("Decrypt Folder", DecryptFolderPage()),
            ("SHA-256 Integrity", IntegrityPage()),
            ("Generate Keys", KeysPage()),
            ("Sign File", SignPage()),
            ("Verify Signature", VerifySignaturePage()),
            ("Encrypt for Receiver", HybridEncryptPage()),
            ("Decrypt Received", HybridDecryptPage()),
            ("Hide Data", HideDataPage()),
            ("Extract Data", ExtractDataPage()),
            ("Secure Delete", SecureDeletePage()),
            ("History", HistoryPage()),
            ("About Vaultix", SettingsPage()),
        ]

        for index, (name, page) in enumerate(page_data):
            button = QPushButton(name)
            button.clicked.connect(lambda checked=False, i=index: self.change_page(i))
            self.nav_buttons.append(button)
            nav_layout.addWidget(button)
            self.pages.addWidget(page)

        nav_layout.addStretch()
        scroll.setWidget(nav_widget)

        sidebar_layout.addWidget(scroll)

        main_layout.addWidget(sidebar_container, 1)
        main_layout.addWidget(self.pages, 5)

    def change_page(self, index):
        self.pages.setCurrentIndex(index)
        self.set_active_button(index)

    def set_active_button(self, active_index):
        for index, button in enumerate(self.nav_buttons):
            button.setProperty("active", index == active_index)
            button.style().unpolish(button)
            button.style().polish(button)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #e5e7eb;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QWidget#sidebar {
                background-color: #020617;
                border-right: 1px solid #1e293b;
            }

            QLabel#logo {
                color: #38bdf8;
                font-size: 26px;
                font-weight: 800;
            }

            QLabel#sidebarSubtitle {
                color: #94a3b8;
                font-size: 12px;
            }

            QLabel#pageTitle {
                color: #38bdf8;
                font-size: 28px;
                font-weight: 800;
            }

            QPushButton {
                background-color: #1e293b;
                color: #f8fafc;
                border: 1px solid #263449;
                border-radius: 9px;
                padding: 10px 12px;
                text-align: left;
                min-height: 20px;
            }

            QPushButton:hover {
                background-color: #2563eb;
                border: 1px solid #3b82f6;
            }

            QPushButton[active="true"] {
                background-color: #0ea5e9;
                color: #020617;
                font-weight: bold;
            }

            QLineEdit, QTextEdit, QSpinBox {
                background-color: #020617;
                color: white;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 9px;
            }

            QTableWidget {
                background-color: #020617;
                color: white;
                border: 1px solid #334155;
                gridline-color: #1e293b;
                selection-background-color: #2563eb;
            }

            QHeaderView::section {
                background-color: #1e293b;
                color: #38bdf8;
                border: 1px solid #334155;
                padding: 8px;
                font-weight: bold;
            }

            QTableCornerButton::section {
                background-color: #1e293b;
                border: 1px solid #334155;
            }

            QScrollArea {
                border: none;
                background-color: transparent;
            }

            QScrollBar:vertical {
                background: #020617;
                width: 8px;
            }

            QScrollBar::handle:vertical {
                background: #334155;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover {
                background: #38bdf8;
            }

            QFrame#dashboardCard {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 14px;
                padding: 14px;
            }

            QLabel#dashboardSubtitle {
                color: #cbd5e1;
                font-size: 15px;
            }

            QLabel#cardTitle {
                color: #94a3b8;
                font-size: 14px;
            }

            QLabel#cardValue {
                color: #38bdf8;
                font-size: 24px;
                font-weight: bold;
            }

            QLabel#cardDescription {
                color: #e5e7eb;
                font-size: 13px;
            }

            QLabel#footerText {
                color: #64748b;
                font-size: 12px;
            }
        """)