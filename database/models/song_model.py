from database.models.model import Model


class SongModel(Model):

    def get_all(self, active_only=False):
        query = """
            SELECT
                songs.*,
                stations.nombre AS station_name
            FROM songs
            INNER JOIN stations
                ON stations.id = songs.station_id
        """

        if active_only:
            query += " WHERE songs.activo = 1"

        query += """
            ORDER BY
                stations.nombre,
                songs.titulo
        """

        with self.database.connect() as connection:
            return connection.execute(query).fetchall()

    def get_by_id(self, song_id):
        query = """
            SELECT
                songs.*,
                stations.nombre AS station_name
            FROM songs
            INNER JOIN stations
                ON stations.id = songs.station_id
            WHERE songs.id = ?
        """

        with self.database.connect() as connection:
            return connection.execute(
                query,
                (song_id,)
            ).fetchone()

    def get_by_station(self, station_id, active_only=False):
        query = """
            SELECT *
            FROM songs
            WHERE station_id = ?
        """

        if active_only:
            query += " AND activo = 1"

        query += " ORDER BY titulo"

        with self.database.connect() as connection:
            return connection.execute(
                query,
                (station_id,)
            ).fetchall()

    def create(
        self,
        titulo,
        tipo,
        numero_himno,
        referencia,
        station_id
    ):
        query = """
            INSERT INTO songs (
                titulo,
                tipo,
                numero_himno,
                referencia,
                station_id,
                activo
            )
            VALUES (?, ?, ?, ?, ?, 1)
        """

        with self.database.connect() as connection:
            cursor = connection.execute(
                query,
                (
                    titulo,
                    tipo,
                    numero_himno,
                    referencia,
                    station_id
                )
            )

            return cursor.lastrowid

    def update(
        self,
        song_id,
        titulo,
        tipo,
        numero_himno,
        referencia,
        station_id
    ):
        query = """
            UPDATE songs
            SET
                titulo = ?,
                tipo = ?,
                numero_himno = ?,
                referencia = ?,
                station_id = ?
            WHERE id = ?
        """

        with self.database.connect() as connection:
            connection.execute(
                query,
                (
                    titulo,
                    tipo,
                    numero_himno,
                    referencia,
                    station_id,
                    song_id
                )
            )

    def set_active(self, song_id, active):
        query = """
            UPDATE songs
            SET activo = ?
            WHERE id = ?
        """

        with self.database.connect() as connection:
            connection.execute(
                query,
                (
                    1 if active else 0,
                    song_id
                )
            )