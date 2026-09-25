from database.models.model import Model


class ProgramType(Model):

    def get_all(self, active_only=False):
        query = """
            SELECT *
            FROM program_types
        """

        if active_only:
            query += " WHERE activo = 1"

        query += " ORDER BY nombre"

        with self.database.connect() as connection:
            return connection.execute(query).fetchall()

    def get_by_id(self, program_type_id):
        with self.database.connect() as connection:
            return connection.execute(
                """
                SELECT *
                FROM program_types
                WHERE id = ?
                """,
                (program_type_id,),
            ).fetchone()

    def create(self, nombre):
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO program_types (nombre, activo)
                VALUES (?, 1)
                """,
                (nombre,),
            )

            return cursor.lastrowid

    def update(self, program_type_id, nombre):
        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE program_types
                SET nombre = ?
                WHERE id = ?
                """,
                (nombre, program_type_id),
            )

    def set_active(self, program_type_id, active):
        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE program_types
                SET activo = ?
                WHERE id = ?
                """,
                (1 if active else 0, program_type_id),
            )
