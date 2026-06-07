from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)

from database.db_manager import get_history, clear_history


class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("History & Audit Logs")
        title.setObjectName("pageTitle")

        refresh_button = QPushButton("Refresh History")
        refresh_button.clicked.connect(self.load_history)

        clear_button = QPushButton("Clear History")
        clear_button.clicked.connect(self.clear_logs)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Action", "Target", "Status", "Date / Time"]
        )

        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(refresh_button)
        layout.addWidget(clear_button)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_history(self):
        records = get_history()

        self.table.setRowCount(len(records))

        for row, record in enumerate(records):
            for col, value in enumerate(record):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.table.resizeColumnsToContents()

    def clear_logs(self):
        confirm = QMessageBox.question(
            self,
            "Clear History",
            "Are you sure you want to clear all history logs?",
        )

        if confirm == QMessageBox.Yes:
            clear_history()
            self.load_history()