from database.database import Database
from views.main_window import MainWindow

from services.selection_service import SelectionService
from services.service_service import ServiceService


def main():
    database = Database()

    selection_service = SelectionService()
    service_service = ServiceService()

    selection = selection_service.generate(1)

    service_id = service_service.confirm_service(
        fecha="2026-11-15",
        program_type_id=1,
        selection=selection
    )

    print("Culto guardado:", service_id)
    
    app = MainWindow(database)
    app.run()


if __name__ == "__main__":
    main()
