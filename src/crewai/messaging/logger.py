"""SQLite logger for agent communications."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Tuple


class CommunicationLogger:
    """Logs messages exchanged between agents into an SQLite database."""

    def __init__(self, db_path: str | Path = "communications.db") -> None:
        """
        Initialize the CommunicationLogger.
        
        Opens (or creates) an SQLite database at `db_path`, stores the connection on the instance, and ensures the required `messages` table exists.
        
        Parameters:
            db_path (str | Path): Filesystem path to the SQLite database file. Defaults to "communications.db".
        """
        self._db_path = Path(db_path)
        self._conn = sqlite3.connect(self._db_path)
        self._create_table()

    def _create_table(self) -> None:
        """
        Ensure the messages table exists in the SQLite database.
        
        Creates a table named `messages` with columns (id INTEGER PRIMARY KEY AUTOINCREMENT, queue TEXT NOT NULL, message TEXT NOT NULL) if it does not already exist. Uses the instance connection's context manager so the CREATE TABLE runs in a transaction (committed on success, rolled back on failure).
        """
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
        """
        Persist a message for a named queue into the SQLite-backed messages table.
        
        Parameters:
        	queue (str): Name of the queue the message belongs to.
        	message (str): Message content to store.
        """
        with self._conn:
            self._conn.execute(
                "INSERT INTO messages (queue, message) VALUES (?, ?)", (queue, message)
            )

    def fetch_all(self) -> List[Tuple[int, str, str]]:
        """
        Return all stored communication messages from the SQLite messages table.
        
        Returns:
            List[Tuple[int, str, str]]: A list of rows, each tuple containing (id, queue, message) where `id` is the auto-incrementing primary key, and `queue` and `message` are stored text fields. The rows are returned in the order provided by the database (no explicit ordering is applied).
        """
        cursor = self._conn.cursor()
        cursor.execute("SELECT id, queue, message FROM messages")
        return cursor.fetchall()

    def close(self) -> None:
        """
        Close the underlying SQLite database connection.
        
        After calling this method the logger's connection is closed and the instance
        should not be used for further database operations.
        """
        self._conn.close()
