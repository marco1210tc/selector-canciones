from database.database import Database
from views.main_window import MainWindow


def main():
    database = Database()
    database.initialize()

    app = MainWindow(database)
    app.run()


if __name__ == "__main__":
    main()
