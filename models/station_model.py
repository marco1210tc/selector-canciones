# from database.database import Database
from models.model import Model


# cargar aqui mismo la conexion del database no hay necesidad de
# pasarle como parametro, se hace my grande el archivo padre
# analizar la posibilidad de que todos los modelos hereden la conexion de una clase padre
class StationModel(Model):
    
    def __init__(self):
        print("creado")

    def get_all(self, active_only=False):
        query = """
            SELECT *
            FROM stations
        """

        params = ()

        if active_only:
            query += " WHERE activo = 1"

        query += " ORDER BY id"

        with self.database.connect() as connection:
            return connection.execute(query, params).fetchall()

    def get_by_id(self, station_id):
        with self.database.connect() as connection:
            return connection.execute(
                """
                SELECT *
                FROM stations
                WHERE id = ?
                """,
                (station_id,),
            ).fetchone()

    def create(self, nombre):
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO stations (
                    nombre,
                    activo
                )
                VALUES (?, 1)
                """,
                (nombre),
            )

            return cursor.lastrowid

    def update(self, station_id, nombre):
        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE stations
                SET nombre = ?,
                WHERE id = ?
                """,
                (nombre, station_id),
            )

    def set_active(self, station_id, active):
        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE stations
                SET activo = ?
                WHERE id = ?
                """,
                (1 if active else 0, station_id),
            )