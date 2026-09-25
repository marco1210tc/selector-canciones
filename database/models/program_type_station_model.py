from database.models.model import Model


class ProgramTypeStationModel(Model):

    def get_all(self):
        query = """
            SELECT *
            FROM program_type_stations
        """
        query += " ORDER BY id"

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