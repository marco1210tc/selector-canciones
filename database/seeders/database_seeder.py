from database.seeders.program_types_seeder import ProgramTypesSeeder
from database.seeders.program_types_stations_seeder import ProgramTypesStationsSeeder
from database.seeders.services_seeder import ServicesSeeder
from database.seeders.songs_seeder import SongsSeeder
from database.seeders.stations_seeder import StationsSeeder


class DatabaseSeeder:
    @staticmethod
    def run(database):
        with database.connect() as connection:
                    # Solo para entorno de pruebas: limpia los datos anteriores.
                    connection.execute("DELETE FROM service_songs")
                    connection.execute("DELETE FROM services")
                    connection.execute("DELETE FROM songs")
                    connection.execute("DELETE FROM program_type_stations")
                    connection.execute("DELETE FROM program_types")
                    connection.execute("DELETE FROM stations")
        
                    station_ids = StationsSeeder.run(connection)
                    program_type_ids = ProgramTypesSeeder.run(connection)
                    ProgramTypesStationsSeeder.run(connection, station_ids, program_type_ids)
                    song_ids_by_station = SongsSeeder.run(connection, station_ids)
                    ServicesSeeder.run(
                        connection, station_ids, program_type_ids, song_ids_by_station
                    )