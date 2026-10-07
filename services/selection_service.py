import random

from database.models.program_type_station_model import ProgramTypeStationModel
from database.models.song_model import SongModel


class SelectionService:
    def __init__(self):
        self.song_model = SongModel()
        self.program_type_station_model = ProgramTypeStationModel()

    def generate(self, program_type_id):
        stations = self.program_type_station_model.get_by_program_type(program_type_id)

        selection = []

        for station in stations:
            songs = self.song_model.get_with_usage(station["station_id"])

            if not songs:
                selection.append(
                    {
                        "station_id": station["station_id"],
                        "station_name": station["station_name"],
                        "song_id": None,
                        "song_title": None,
                        "tipo": None,
                        "numero_himno": None,
                        "referencia": None,
                        "available": False,
                    }
                )
                continue

            best_songs = self._get_best_candidates(songs)

            selected_song = random.choice(best_songs)

            selection.append(
                {
                    "station_id": station["station_id"],
                    "station_name": station["station_name"],
                    "song_id": selected_song["id"],
                    "song_title": selected_song["titulo"],
                    "tipo": selected_song["tipo"],
                    "numero_himno": selected_song["numero_himno"],
                    "referencia": selected_song["referencia"],
                    "available": True,
                }
            )

        return selection

    def _get_best_candidates(self, songs):
        best_usage_count = min(song["usage_count"] for song in songs)

        candidates = [song for song in songs if song["usage_count"] == best_usage_count]

        oldest_date = min(
            (
                song["last_used_date"]
                for song in candidates
                if song["last_used_date"] is not None
            ),
            default=None,
        )

        if oldest_date is None:
            return candidates

        return [song for song in candidates if song["last_used_date"] == oldest_date]
