from database.database import Database
from database.seeders.stations_seeder import StationsSeeder


class DatabaseSeeder:

    @staticmethod
    def run(database: Database):
        StationsSeeder.run(database)