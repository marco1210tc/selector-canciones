
from database.models.service_model import ServiceModel
from database.models.service_song_model import ServiceSongModel


class ServiceService:

    def __init__(self):
        self.service_model = ServiceModel()
        self.service_song_model = ServiceSongModel()

    def confirm_service(self, fecha, program_type_id, selection):

        if not fecha:
            raise ValueError("La fecha del culto es obligatoria.")

        if not program_type_id:
            raise ValueError("Debe seleccionar un tipo de programa.")

        if not selection:
            raise ValueError("La selección del culto está vacía.")

        # Validar que todas las estaciones tengan canción.
        for item in selection:
            if not item.get("song_id"):
                raise ValueError(
                    f'La estación "{item["station_name"]}" '
                    "no tiene una canción seleccionada."
                )

        # Guardar todo dentro de una única transacción.
        with self.service_model.database.connect() as connection:

            cursor = connection.execute(
                """
                INSERT INTO services (fecha, program_type_id)
                VALUES (?, ?)
                """,
                (fecha, program_type_id)
            )

            service_id = cursor.lastrowid

            for item in selection:
                connection.execute(
                    """
                    INSERT INTO service_songs (
                        service_id,
                        station_id,
                        song_id
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        service_id,
                        item["station_id"],
                        item["song_id"]
                    )
                )

            return service_id
