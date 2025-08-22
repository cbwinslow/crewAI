"""SQLite logger for agent communications."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Tuple


class CommunicationLogger:
    """Logs messages exchanged between agents into an SQLite database."""

    def __init__(self, db_path: str | Path = "communications.db") -> None:
        self._db_path = Path(db_path)
        self._conn = sqlite3.connect(self._db_path)
        self._create_table()

    def _create_table(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    queue TEXT NOT NULL,
                    message TEXT NOT NULL
                )
                """
            )

    def log(self, queue: str, message: str) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT INTO messages (queue, message) VALUES (?, ?)", (queue, message)
            )

    def fetch_all(self) -> List[Tuple[int, str, str]]:
        cursor = self._conn.cursor()
        cursor.execute("SELECT id, queue, message FROM messages")
        return cursor.fetchall()

    def close(self) -> None:
        self._conn.close()
