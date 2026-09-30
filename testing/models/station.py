from database.models.station_model import StationModel


def get_all():
  station_model = StationModel()
  for row in station_model.get_all():
    print(row["id"], row["nombre"], row["activo"])