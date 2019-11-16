import sqlite3

import os


class Sqlite3db:
    def __init__(self, sqlite_file):
        self.sqlite_conn = sqlite3.connect(sqlite_file)
        self.sqlite_conn.text_factory = str

    def get_coon(self):
        return self.sqlite_conn

    def commit(self):
        self.sqlite_conn.commit()

    def __del__(self):
        self.sqlite_conn.close()

# sqlite3db = Sqlite3db()
