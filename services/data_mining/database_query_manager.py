from database import Database


class DatabaseQueryManager:
    def __init__(self):
        self._db = Database()

    def write_shows_data(self, data):
        self._db.write("shows", data, "insert", "id")
