from database.models.model import Model


class ServiceSongModel(Model):

    def get_by_service(self, service_id):
        query = """
            SELECT
                service_songs.*,
                songs.titulo AS song_title,
                stations.nombre AS station_name
            FROM service_songs
            INNER JOIN songs
                ON songs.id = service_songs.song_id
            INNER JOIN stations
                ON stations.id = service_songs.station_id
            WHERE service_songs.service_id = ?
            ORDER BY stations.nombre
        """

        with self.database.connect() as connection:
            return connection.execute(
                query,
                (service_id,)
            ).fetchall()

    def add(
        self,
        service_id,
        station_id,
        song_id
    ):
        query = """
            INSERT INTO service_songs (
                service_id,
                station_id,
                song_id
            )
            VALUES (?, ?, ?)
        """

        with self.database.connect() as connection:
            cursor = connection.execute(
                query,
                (
                    service_id,
                    station_id,
                    song_id
                )
            )

            return cursor.lastrowid

    def get_song_history(self, song_id):
        query = """
            SELECT
                services.id AS service_id,
                services.fecha,
                service_songs.station_id
            FROM service_songs
            INNER JOIN services
                ON services.id = service_songs.service_id
            WHERE service_songs.song_id = ?
            ORDER BY services.fecha DESC
        """

        with self.database.connect() as connection:
            return connection.execute(
                query,
                (song_id,)
            ).fetchall()