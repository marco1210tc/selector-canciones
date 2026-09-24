from database.seeders.stations_seeder import StationsSeeder
from database.seeders.program_types_seeder import ProgramTypesSeeder
from database.seeders.program_types_stations_seeder import ProgramTypesStationsSeeder


class DatabaseSeeder:

    @staticmethod
    def run(database):

        with database.connect() as connection:

            station_ids = StationSeeder.run(connection)

            program_type_ids = ProgramTypeSeeder.run(connection)

            ProgramTypeStationSeeder.run(
                connection,
                station_ids,
                program_type_ids
            )