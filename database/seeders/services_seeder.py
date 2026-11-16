from datetime import date, timedelta
import random


class ServicesSeeder:
    @staticmethod
    def run(connection, station_ids, program_type_ids, song_ids_by_station):
        # Ocho programas de ejemplo en domingos consecutivos.
        first_sunday = date(2026, 9, 27)
        rng = random.Random(2026)
        for index in range(8):
            service_date = first_sunday + timedelta(days=7 * index)
            program_name = "Cena del Señor" if index in (1, 5) else "Culto normal"
            program_type_id = program_type_ids[program_name]
            cursor = connection.execute(
                "INSERT INTO services (fecha, program_type_id) VALUES (?, ?)",
                (service_date.isoformat(), program_type_id),
            )
            service_id = cursor.lastrowid
            station_rows = connection.execute(
                """SELECT s.nombre
                   FROM program_type_stations pts
                   JOIN stations s ON s.id = pts.station_id
                   WHERE pts.program_type_id = ?
                   ORDER BY pts.orden""",
                (program_type_id,),
            ).fetchall()
            for station_row in station_rows:
                station_name = station_row["nombre"]
                available = song_ids_by_station.get(station_name, [])
                if not available:
                    continue
                song_id = rng.choice(available)
                connection.execute(
                    """INSERT INTO service_songs (service_id, station_id, song_id)
                       VALUES (?, ?, ?)""",
                    (service_id, station_ids[station_name], song_id),
                )
