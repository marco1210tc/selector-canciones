from database.database import Database


class Model:
  database = Database()

# def get_by_id(self, station_id, table_name):  implementar más adelante
#   with self.database.connect() as connection:
#     return connection.execute(
#         """
#           SELECT *
#           FROM table_name = ?
#           WHERE id = ?
#           """,
#         (station_id, table_name),
#     ).fetchone()

    # def __init__(self):
    #   self.connection = self.db_connection.connect()
    # def connect(self):
    #   return self.connection

    # def __del__(self):
    #   self.connection.close()

    # def commit(self):
    #   self.connection.commit()
