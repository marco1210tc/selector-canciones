from database.database import Database


class ProgramTypeSeeder:

    program_types = [
        "Culto normal",
        "Santa Cena",
    ]

    @classmethod
    def run(cls, database: Database):
        with database.connect() as connection:
            for nombre in cls.program_types:
                connection.execute(
                    """
                    INSERT INTO program_types (
                        nombre,
                        activo
                    )
                    VALUES (?, 1)
                    """,
                    (nombre,) 
            )