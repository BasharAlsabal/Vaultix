import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import VaultixMainWindow


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("Vaultix")
    app.setOrganizationName("Bashar Alsabal")

    window = VaultixMainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()