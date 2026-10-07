from database.models.song_model import SongModel
from database.models.station_model import StationModel


class SongService:
    def __init__(self):
        self.song_model = SongModel()
        self.station_model = StationModel()

    def get_all_songs(self, active_only=False):
        return self.song_model.get_all(active_only)

    def get_song_by_id(self, song_id):
        return self.song_model.get_by_id(song_id)

    def get_all_stations(self, active_only=False):
        return self.station_model.get_all(active_only)

    def get_station_by_id(self, station_id):
        return self.station_model.get_by_id(station_id)

    def _prepare_song_data(self, tipo, numero_himno):
        if tipo not in self.song_model.tipos:
            raise ValueError("El tipo de canción no es válido.")

        if tipo == "himno":
            if not numero_himno:
                raise ValueError("El himno debe tener un número.")

            try:
                numero_himno = int(numero_himno)
            except ValueError:
                raise ValueError("El número de himno debe ser un número entero.")

            if numero_himno <= 0:
                raise ValueError("El número de himno debe ser mayor que cero.")

            return numero_himno, "Himnario"

        return None, "Folder"

    def create(self, titulo, tipo, numero_himno, station_id):
        titulo = titulo.strip().upper()
        tipo = tipo.strip().lower()

        if not titulo:
            raise ValueError("El título es obligatorio.")

        if not station_id:
            raise ValueError("Debe seleccionar una estación.")
        
        numero_himno, referencia = self._prepare_song_data(tipo, numero_himno)

        return self.song_model.create(
            titulo=titulo,
            tipo=tipo,
            numero_himno=numero_himno,
            referencia=referencia,
            station_id=station_id,
        )

    def update(self, song_id, titulo, tipo, numero_himno, station_id):
        titulo = titulo.strip().upper()
        tipo = tipo.strip().lower()

        if not titulo:
            raise ValueError("El título es obligatorio.")

        if not station_id:
            raise ValueError("Debe seleccionar una estación.")

        if tipo not in ("himno", "alabanza"):
            raise ValueError("El tipo de canción no es válido.")

        numero_himno, referencia = self._prepare_song_data(tipo, numero_himno)

        self.song_model.update(
            song_id=song_id,
            titulo=titulo,
            tipo=tipo,
            numero_himno=numero_himno,
            referencia=referencia,
            station_id=station_id,
        )

    def set_active(self, song_id, active):
        self.song_model.set_active(song_id, active)
