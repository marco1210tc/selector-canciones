from database.database import Database
from database.seeders.database_seeder import DatabaseSeeder


def main():
    database = Database()

    database.initialize()
    DatabaseSeeder.run(database)

    print("Base de datos inicializada correctamente.")
    print("Seeders ejecutados correctamente.")

if __name__ == "__main__":
    main()