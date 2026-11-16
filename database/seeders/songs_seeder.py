from database.seeders.songs_data import SONGS

class SongsSeeder:
    @staticmethod
    def run(connection, station_ids):
        song_ids_by_station = {}
        for song in SONGS:
            cursor = connection.execute(
                """INSERT INTO songs
                   (titulo, tipo, numero_himno, referencia, station_id, activo)
                   VALUES (?, ?, ?, ?, ?, 1)""",
                (song["titulo"], song["tipo"], song["numero_himno"],
                 song["referencia"], station_ids[song["station"]])
            )
            song_ids_by_station.setdefault(song["station"], []).append(cursor.lastrowid)
        return song_ids_by_station