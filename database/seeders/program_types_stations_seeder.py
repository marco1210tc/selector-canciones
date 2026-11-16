NORMAL_STATIONS = [
    "Adoración", "Consagración", "Comunión", "Glorificación",
    "Intercesión", "Predicación", "Dádivas", "Comisión", "Expectación"
]
# Configuración provisional para pruebas: Cena del Señor utiliza las primeras seis estaciones.
LORDS_SUPPER_STATIONS = NORMAL_STATIONS[:6]

class ProgramTypesStationsSeeder:
    @staticmethod
    def run(connection, station_ids, program_type_ids):
        mapping = {
            "Culto normal": NORMAL_STATIONS,
            "Cena del Señor": LORDS_SUPPER_STATIONS,
        }
        for program_name, station_names in mapping.items():
            for orden, station_name in enumerate(station_names, start=1):
                connection.execute(
                    """INSERT INTO program_type_stations
                       (program_type_id, station_id, orden) VALUES (?, ?, ?)""",
                    (program_type_ids[program_name], station_ids[station_name], orden)
                )
