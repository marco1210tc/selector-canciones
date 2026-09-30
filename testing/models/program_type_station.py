from database.models.program_type_station_model import ProgramTypeStationModel


def get_all():
  program_type_station_model = ProgramTypeStationModel()
  for row in program_type_station_model.get_all():
    print(row["id"], row["program_type_id"], row["station_id"], row["orden"])

def get_by_program_type():
  program_type_station_model = ProgramTypeStationModel()
  for row in program_type_station_model.get_by_program_type(1):
    print(row["id"], row["program_type_id"], row["station_id"], row["orden"], row["station_name"])
