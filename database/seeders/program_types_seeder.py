class ProgramTypesSeeder:

    program_types = [
        "Culto normal",
        "Cena del Señor",
    ]

    @classmethod
    def run(cls, connection):

        program_type_ids = {}

        for nombre in cls.program_types:

            cursor = connection.execute(
                """
                INSERT INTO program_types (
                    nombre,
                    activo
                )
                VALUES (?, 1)
                """,
                (nombre,)
            )

            program_type_ids[nombre] = cursor.lastrowid

        return program_type_ids