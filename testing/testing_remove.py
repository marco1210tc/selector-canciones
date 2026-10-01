from database.models.program_type_station_model import ProgramTypeStationModel


def mostrar(model, program_type_id):
    rows = model.get_by_program_type(program_type_id)

    print("\nEstaciones del programa:")

    for row in rows:
        print(
            f'{row["orden"]}. '
            f'{row["station_name"]} '
            f'(station_id={row["station_id"]}, '
            f'pts_id={row["id"]})'
        )


def main():

    model = ProgramTypeStationModel()

    program_type_id = 2

    print("=== ESTADO INICIAL ===")
    mostrar(model, program_type_id)

    # --------------------------------------------------
    # 1. REORDENAR
    # --------------------------------------------------

    print("\n=== REORDENANDO ===")

    rows = model.get_by_program_type(program_type_id)

    station_ids = [row["station_id"] for row in rows]

    # Intercambiamos las dos primeras estaciones.
    station_ids[0], station_ids[1] = (
        station_ids[1],
        station_ids[0]
    )

    model.reorder(
        program_type_id,
        station_ids
    )

    mostrar(model, program_type_id)

    # --------------------------------------------------
    # 2. AGREGAR
    # --------------------------------------------------

    print("\n=== AGREGANDO ESTACIÓN ===")

    # Primero obtenemos una estación que todavía
    # no esté en el programa.
    existing_rows = model.get_by_program_type(program_type_id)

    existing_station_ids = {
        row["station_id"]
        for row in existing_rows
    }

    # Las estaciones del seed tienen IDs 1..9.
    available_station_id = next(
        station_id
        for station_id in range(1, 10)
        if station_id not in existing_station_ids
    )

    new_order = len(existing_rows) + 1

    model.add_station(
        program_type_id,
        available_station_id,
        new_order
    )

    mostrar(model, program_type_id)

    # --------------------------------------------------
    # 3. ELIMINAR
    # --------------------------------------------------

    print("\n=== ELIMINANDO LA ÚLTIMA ESTACIÓN ===")

    rows = model.get_by_program_type(program_type_id)

    last_row = rows[-1]

    model.remove_station(last_row["id"])

    mostrar(model, program_type_id)


if __name__ == "__main__":
    main()