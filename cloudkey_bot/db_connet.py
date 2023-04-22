import sqlite3


class SQLiteConnect:

    def __init__(self, path: str):
        self.path = path

    def login(self):
        connect = sqlite3.connect(self.path)
        return connect
