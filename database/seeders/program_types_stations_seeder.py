class ProgramTypesStationsSeeder:

    programs = {
        "Culto normal": [
            "Adoración",
            "Consagración",
            "Comunión",
            "Glorificación",
            "Intercesión",
            "Predicación",
            "Dádivas",
            "Comisión",
            "Expectación",
        ],

        "Cena del Señor": [
            "Adoración",
            "Consagración",
            "Comunión",
            "Intercesión",
            "Predicación",
            "Expectación",
        ],
    }

    @classmethod
    def run(
        cls,
        connection,
        station_ids,
        program_type_ids
    ):

        for program_name, stations in cls.programs.items():

            program_type_id = program_type_ids[program_name]

            for orden, station_name in enumerate(stations, start=1):

                station_id = station_ids[station_name]

                connection.execute(
                    """
                    INSERT INTO program_type_stations (
                        program_type_id,
                        station_id,
                        orden
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        program_type_id,
                        station_id,
                        orden
                    )
                )