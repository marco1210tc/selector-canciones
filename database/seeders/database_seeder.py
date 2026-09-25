from database.seeders.program_types_seeder import ProgramTypesSeeder
from database.seeders.program_types_stations_seeder import ProgramTypesStationsSeeder
from database.seeders.stations_seeder import StationsSeeder


class DatabaseSeeder:
    @staticmethod
    def run(database):

        with database.connect() as connection:
            station_ids = StationsSeeder.run(connection)

            program_type_ids = ProgramTypesSeeder.run(connection)

            ProgramTypesStationsSeeder.run(connection, station_ids, program_type_ids)
