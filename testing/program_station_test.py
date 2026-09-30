from testing.models.program_type_station import *


class ProgramTypeStationTest:

  class Get:
    def get_all(self, program_type_id):
        print("Testeando ProgramTypeStationModel id = 1 >>>>>>")
        get_by_program_type(program_type_id)

  class Remove:
    def test(self, station_id):
        print(f"Testeando Remove estation id = {station_id} >>>>>>")
        remove_station(station_id)

  class Add:
    def test(self, program_type_id, station_id, orden):
        print("Testeando Add estation id = ? >>>>>>")
        add_station(program_type_id, station_id, orden)