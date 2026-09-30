from database.database import Database
from database.models.program_type_station_model import ProgramTypeStationModel
from views.main_window import MainWindow


def main():
    database = Database()

    app = MainWindow(database)
    app.run()


if __name__ == "__main__":
    main()
