from database.database import Database


class StationsSeeder:

    stations = [
        "Adoración",
        "Consagración",
        "Comunión",
        "Glorificación",
        "Intercesión",
        "Predicación",
        "Dádivas",
        "Comisión",
        "Expectación",
    ]

    @classmethod
    def run(cls, database: Database):
        with database.connect() as connection:

            for nombre in cls.stations: 
                connection.execute(
                    """
                    INSERT INTO stations (nombre, activo)
                    VALUES (?, 1)
                    """,
                    (nombre, )
                )