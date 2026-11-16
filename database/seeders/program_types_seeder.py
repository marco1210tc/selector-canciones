PROGRAM_TYPES = ["Culto normal", "Cena del Señor"]

class ProgramTypesSeeder:
    @staticmethod
    def run(connection):
        ids = {}
        for nombre in PROGRAM_TYPES:
            cursor = connection.execute(
                "INSERT INTO program_types (nombre, activo) VALUES (?, 1)", (nombre,)
            )
            ids[nombre] = cursor.lastrowid
        return ids