"""Puente Python ↔ JavaScript. Las vistas web no acceden a SQLite directamente."""
import sqlite3
from datetime import date

from database.database import Database
from database.models.program_type_model import ProgramTypeModel
from database.models.program_type_station_model import ProgramTypeStationModel
from database.models.service_model import ServiceModel
from database.models.service_song_model import ServiceSongModel
from database.models.station_model import StationModel
from services.selection_service import SelectionService
from services.service_service import ServiceService
from services.song_service import SongService


def serial(rows):
    if rows is None:
        return None
    if isinstance(rows, (list, tuple)):
        return [dict(r) for r in rows]
    return dict(rows)


class Api:
    def __init__(self):
        self.db = Database()
        self.stations = StationModel()
        self.types = ProgramTypeModel()
        self.config = ProgramTypeStationModel()
        self.songs = SongService()
        self.selection = SelectionService()
        self.services = ServiceService()
        self.service_model = ServiceModel()
        self.service_songs = ServiceSongModel()

    def _call(self, fn):
        try:
            return {'ok': True, 'data': fn()}
        except (ValueError, sqlite3.IntegrityError) as exc:
            return {'ok': False, 'error': str(exc)}
        except Exception as exc:
            # Evita bloquear la interfaz por errores inesperados.
            return {'ok': False, 'error': f'Error de operación: {exc}'}

    def initial_data(self):
        return self._call(lambda: {
            'stations': serial(self.stations.get_all()),
            'types': serial(self.types.get_all()),
            'songs': serial(self.songs.get_all_songs()),
            'services': self._get_services(),
        })

    def list_stations(self):
        return self._call(lambda: serial(self.stations.get_all()))

    def save_station(self, payload):
        def work():
            name = str(payload.get('nombre', '')).strip()
            if not name:
                raise ValueError('El nombre de la estación es obligatorio.')
            if payload.get('id'):
                self.stations.update(int(payload['id']), name)
                return int(payload['id'])
            return self.stations.create(name)
        return self._call(work)

    def set_station_active(self, station_id, active):
        return self._call(lambda: self.stations.set_active(int(station_id), bool(active)))

    def list_types(self):
        return self._call(lambda: serial(self.types.get_all()))

    def save_type(self, payload):
        def work():
            name = str(payload.get('nombre', '')).strip()
            if not name:
                raise ValueError('El nombre del tipo de programa es obligatorio.')
            if payload.get('id'):
                self.types.update(int(payload['id']), name)
                return int(payload['id'])
            return self.types.create(name)
        return self._call(work)

    def set_type_active(self, type_id, active):
        return self._call(lambda: self.types.set_active(int(type_id), bool(active)))

    def get_type_stations(self, type_id):
        return self._call(lambda: serial(self.config.get_by_program_type(int(type_id))))

    def save_type_stations(self, type_id, station_ids):
        def work():
            ids = [int(x) for x in station_ids]
            if len(ids) != len(set(ids)):
                raise ValueError('No se puede repetir una estación.')
            active = {int(s['id']) for s in self.stations.get_all(active_only=True)}
            if not set(ids).issubset(active):
                raise ValueError('Solo pueden agregarse estaciones activas.')
            self.config.save_configuration(int(type_id), ids)
            return True
        return self._call(work)

    def list_songs(self):
        return self._call(lambda: serial(self.songs.get_all()))

    def songs_by_station(self, station_id):
        return self._call(lambda: serial(self.songs.get_by_station(int(station_id), active_only=True)))

    def save_song(self, payload):
        def work():
            params = dict(
                titulo=str(payload.get('titulo', '')).strip(),
                tipo=str(payload.get('tipo', '')),
                numero_himno=payload.get('numero_himno'),
                station_id=int(payload['station_id']) if payload.get('station_id') else None,
            )
            if payload.get('id'):
                self.songs.update(song_id=int(payload['id']), **params)
                return int(payload['id'])
            return self.songs.create(**params)
        return self._call(work)

    def set_song_active(self, song_id, active):
        return self._call(lambda: self.songs.set_active(int(song_id), bool(active)))

    def generate(self, type_id):
        def work():
            program = self.types.get_by_id(int(type_id))
            if program is None or not program['activo']:
                raise ValueError('Selecciona un tipo de programa activo.')
            return serial(self.selection.generate(int(type_id)))
        return self._call(work)

    def confirm(self, payload):
        def work():
            fecha = str(payload.get('fecha', ''))
            try:
                date.fromisoformat(fecha)
            except ValueError:
                raise ValueError('La fecha debe ser válida y usar YYYY-MM-DD.')
            type_id = int(payload['program_type_id'])
            type_row = self.types.get_by_id(type_id)
            if type_row is None:
                raise ValueError('El tipo de programa no existe.')
            rows = payload.get('selection', [])
            configured = self.config.get_by_program_type(type_id)
            expected = {int(r['station_id']) for r in configured}
            actual = [int(r['station_id']) for r in rows]
            if not expected or len(actual) != len(expected) or set(actual) != expected:
                raise ValueError('La selección no coincide con las estaciones configuradas.')
            for item in rows:
                if not item.get('song_id'):
                    raise ValueError('Todas las estaciones deben tener canción.')
            # Comprobar pertenencia y estado desde la BD, no confiar en el navegador.
            with self.db.connect() as con:
                for item in rows:
                    found = con.execute(
                        'SELECT 1 FROM songs WHERE id=? AND station_id=? AND activo=1',
                        (int(item['song_id']), int(item['station_id']))
                    ).fetchone()
                    if not found:
                        raise ValueError('Existe una canción inactiva o de otra estación.')
            return self.services.confirm_service(fecha, type_id, rows)
        return self._call(work)

    def _get_services(self):
        with self.db.connect() as con:
            return serial(con.execute('''
                SELECT s.id, s.fecha, s.program_type_id,
                       p.nombre AS program_type_name,
                       COUNT(ss.id) AS station_count
                FROM services s
                JOIN program_types p ON p.id=s.program_type_id
                LEFT JOIN service_songs ss ON ss.service_id=s.id
                GROUP BY s.id
                ORDER BY s.fecha DESC, s.id DESC
            ''').fetchall())

    def list_services(self):
        return self._call(self._get_services)

    def get_service(self, service_id):
        def work():
            with self.db.connect() as con:
                service = con.execute('''
                    SELECT s.id, s.fecha, s.program_type_id,
                           p.nombre AS program_type_name
                    FROM services s JOIN program_types p ON p.id=s.program_type_id
                    WHERE s.id=?
                ''', (int(service_id),)).fetchone()
                if service is None:
                    raise ValueError('El culto no existe.')
                songs = con.execute('''
                    SELECT ss.station_id, ss.song_id, st.nombre AS station_name,
                           so.titulo AS song_title, so.tipo, so.numero_himno, so.referencia
                    FROM service_songs ss
                    JOIN songs so ON so.id=ss.song_id
                    JOIN stations st ON st.id=ss.station_id
                    LEFT JOIN program_type_stations pts
                      ON pts.program_type_id=? AND pts.station_id=ss.station_id
                    WHERE ss.service_id=?
                    ORDER BY pts.orden, ss.id
                ''', (service['program_type_id'], int(service_id))).fetchall()
                return {'service': dict(service), 'songs': serial(songs)}
        return self._call(work)
