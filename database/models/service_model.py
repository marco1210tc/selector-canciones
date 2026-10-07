from database.models.model import Model


class ServiceModel(Model):

    def get_all(self):
        query = """
            SELECT
                services.*,
                program_types.nombre AS program_type_name
            FROM services
            INNER JOIN program_types
                ON program_types.id = services.program_type_id
            ORDER BY services.fecha DESC
        """

        with self.database.connect() as connection:
            return connection.execute(query).fetchall()

    def get_by_id(self, service_id):
        query = """
            SELECT
                services.*,
                program_types.nombre AS program_type_name
            FROM services
            INNER JOIN program_types
                ON program_types.id = services.program_type_id
            WHERE services.id = ?
        """

        with self.database.connect() as connection:
            return connection.execute(
                query,
                (service_id,)
            ).fetchone()

    def get_by_date(self, fecha):
        query = """
            SELECT *
            FROM services
            WHERE fecha = ?
        """

        with self.database.connect() as connection:
            return connection.execute(
                query,
                (fecha,)
            ).fetchone()

    def create(self, fecha, program_type_id):
        query = """
            INSERT INTO services (
                fecha,
                program_type_id
            )
            VALUES (?, ?)
        """

        with self.database.connect() as connection:
            cursor = connection.execute(
                query,
                (fecha, program_type_id)
            )

            return cursor.lastrowid