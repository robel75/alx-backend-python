import sqlite3

class DatabaseConnection:
    def init(self, db_name):
        self.db_name = db_name
        self.conn = None

    def enter(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # This is what "as conn" gives you in the with-block

    def exit(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()  # Always close connection
