import sqlite3
from pathlib import Path


class Database:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.db_path = self.base_dir / "culto.db"

    def connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection