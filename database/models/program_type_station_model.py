from database.models.model import Model


class ProgramTypeStationModel(Model):

    def get_all(self):
        query = """
            SELECT *
            FROM program_type_stations
        """

        with self.database.connect() as connection:
            return connection.execute(query, ()).fetchall()

    def get_by_program_type(self, program_type_id):
        query = """
            SELECT
                pts.id,
                pts.program_type_id,
                pts.station_id,
                pts.orden,
                s.nombre AS station_name
            FROM program_type_stations pts
            JOIN stations s
                ON s.id = pts.station_id
            WHERE pts.program_type_id = ?
            ORDER BY pts.orden
        """

        with self.database.connect() as connection:
            return connection.execute(
                query,
                (program_type_id,)
            ).fetchall()

    def add_station(self, program_type_id, station_id, orden):
        query = """
            INSERT INTO program_type_stations (
                program_type_id,
                station_id,
                orden
            )
            VALUES (?, ?, ?)
        """

        with self.database.connect() as connection:
            cursor = connection.execute(
                query,
                (program_type_id, station_id, orden)
            )

            return cursor.lastrowid

    def remove_station(self, program_type_station_id):
        with self.database.connect() as connection:

            # Primero obtenemos el programa y el orden de la estación.
            row = connection.execute(
                """
                SELECT program_type_id, orden
                FROM program_type_stations
                WHERE id = ?
                """,
                (program_type_station_id,)
            ).fetchone()

            if row is None:
                return False

            program_type_id = row["program_type_id"]
            orden_eliminado = row["orden"]

            # Eliminamos la relación.
            connection.execute(
                """
                DELETE FROM program_type_stations
                WHERE id = ?
                """,
                (program_type_station_id,)
            )

            # Corregimos los órdenes posteriores.
            connection.execute(
                """
                UPDATE program_type_stations
                SET orden = orden - 1
                WHERE program_type_id = ?
                AND orden > ?
                """,
                (program_type_id, orden_eliminado)
            )

            return True

    def reorder(self, program_type_id, station_ids):

        with self.database.connect() as connection:

            rows = connection.execute(
                """
                SELECT station_id
                FROM program_type_stations
                WHERE program_type_id = ?
                """,
                (program_type_id,)
            ).fetchall()

            current_station_ids = {
                row["station_id"]
                for row in rows
            }

            new_station_ids = set(station_ids)

            # Comprobamos que no falte ni sobre ninguna estación.
            if current_station_ids != new_station_ids:
                raise ValueError(
                    "Las estaciones proporcionadas no coinciden "
                    "con las estaciones actuales del programa."
                )

            # Primera fase: órdenes temporales.
            connection.execute(
                """
                UPDATE program_type_stations
                SET orden = -orden
                WHERE program_type_id = ?
                """,
                (program_type_id,)
            )

            # Segunda fase: asignamos el nuevo orden.
            for orden, station_id in enumerate(station_ids, start=1):
                connection.execute(
                    """
                    UPDATE program_type_stations
                    SET orden = ?
                    WHERE program_type_id = ?
                    AND station_id = ?
                    """,
                    (
                        orden,
                        program_type_id,
                        station_id
                    )
                )