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
    def run(cls, connection):

        station_ids = {}

        for nombre in cls.stations:

            cursor = connection.execute(
                """
                INSERT INTO stations (
                    nombre,
                    activo
                )
                VALUES (?, 1)
                """,
                (nombre,)
            )

            station_ids[nombre] = cursor.lastrowid

        return station_ids