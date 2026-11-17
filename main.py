from view import View

from api import Api
from database.database import Database
from services.selection_service import SelectionService
from services.service_service import ServiceService


def main():
    
    database = Database()

    selection_service = SelectionService()
    service_service = ServiceService()

    app = View(api=Api())
    # app = MainWindow(database)
    # app.run()


if __name__ == "__main__":
    main()
