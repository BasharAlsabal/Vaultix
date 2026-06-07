import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = Path("vaultix_history.db")


def init_database():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                target TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.commit()


def add_history(action: str, target: str, status: str):
    init_database()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO history (action, target, status, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                action,
                target,
                status,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

        conn.commit()


def get_history():
    init_database()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT action, target, status, created_at
            FROM history
            ORDER BY id DESC
        """)

        return cursor.fetchall()


def clear_history():
    init_database()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM history")
        conn.commit()

def get_dashboard_stats():
    init_database()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM history")
        total_operations = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM history WHERE action = 'Encrypt File'")
        encrypted_files = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM history WHERE action = 'Decrypt File'")
        decrypted_files = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM history WHERE action = 'Secure Delete'")
        secure_deletes = cursor.fetchone()[0]

        return {
            "total_operations": total_operations,
            "encrypted_files": encrypted_files,
            "decrypted_files": decrypted_files,
            "secure_deletes": secure_deletes,
        }        