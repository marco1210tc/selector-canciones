STATIONS = [
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


class StationsSeeder:
    @staticmethod
    def run(connection):
        ids = {}
        for orden, nombre in enumerate(STATIONS, start=1):
            cursor = connection.execute(
                "INSERT INTO stations (nombre, activo) VALUES (?, 1)", (nombre,)
            )
            ids[nombre] = cursor.lastrowid
        return ids
