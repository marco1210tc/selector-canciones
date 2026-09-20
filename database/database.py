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

    def initialize(self):
        with self.connect() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS stations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    activo INTEGER NOT NULL DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS program_types (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    activo INTEGER NOT NULL DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS program_type_stations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    program_type_id INTEGER NOT NULL,
                    station_id INTEGER NOT NULL,
                    orden INTEGER NOT NULL,

                    FOREIGN KEY (program_type_id)
                        REFERENCES program_types(id)
                        ON DELETE CASCADE,

                    FOREIGN KEY (station_id)
                        REFERENCES stations(id)
                        ON DELETE RESTRICT,

                    UNIQUE(program_type_id, station_id),
                    UNIQUE(program_type_id, orden)
                );

                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    tipo TEXT NOT NULL CHECK (tipo IN ('himno', 'alabanza')),
                    numero_himno INTEGER,
                    referencia TEXT NOT NULL,
                    orden INTEGER NOT NULL,
                    station_id INTEGER NOT NULL,
                    activo INTEGER NOT NULL DEFAULT 1,

                    FOREIGN KEY (station_id)
                        REFERENCES stations(id)
                        ON DELETE RESTRICT
                );

                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL UNIQUE,
                    program_type_id INTEGER NOT NULL,

                    FOREIGN KEY (program_type_id)
                        REFERENCES program_types(id)
                        ON DELETE RESTRICT
                );

                CREATE TABLE IF NOT EXISTS service_songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_id INTEGER NOT NULL,
                    station_id INTEGER NOT NULL,
                    song_id INTEGER NOT NULL,

                    FOREIGN KEY (service_id)
                        REFERENCES services(id)
                        ON DELETE CASCADE,

                    FOREIGN KEY (station_id)
                        REFERENCES stations(id)
                        ON DELETE RESTRICT,

                    FOREIGN KEY (song_id)
                        REFERENCES songs(id)
                        ON DELETE RESTRICT,

                    UNIQUE(service_id, station_id)
                );
            """)