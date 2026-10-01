from testing.program_station_test import ProgramTypeStationTest
from testing.station_test import StationTest


def program_type_tests():
  t = ProgramTypeStationTest()
  #Get all
  get_program_sections = t.Get()
  get_program_sections.get_all(program_type_id=1)

  # Add
  add_station = t.Add()
  add_station.test(program_type_id=1, station_id=10, orden=10)
  
  #Remove
  # remove_station = t.Remove()
  # remove_station.test(station_id=10)

def station_tests():
  s = StationTest()

  #Get all
  get_stations = s.Get() #probar con factories para cada test de cada metodo: get, update, delete, add
  get_stations.get()

def main():
  # program_type_tests()
  station_tests()


if __name__ == "__main__":

  main()