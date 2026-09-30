from database.models.program_type_station_model import ProgramTypeStationModel
from testing.models.program_type_station import *


class Test:
  def test(self):
      obj = ProgramTypeStationModel()
      print("Testeando ProgramTypeStationModel id = 1 >>>>>>")
      self.imprimir(obj.get_by_program_type(1))
      # print("Testeando ProgramTypeStationModel id = 2 >>>>>>")
      # self.imprimir(obj.get_by_program_type(2))

  def imprimir(self, lista):
    for row in lista:
      print(row["id"], row["program_type_id"], row["station_id"], row["orden"], row["station_name"])
