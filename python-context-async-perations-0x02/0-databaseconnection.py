import sqlite3

class DatabaseConnection:
    # This is the init method
    def _init_(self, db_name):
        self.db_name = db_name
        self.conn = None

    # This is the enter method
    def _enter_(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    # This is the exit method
    def _exit_(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# Using the context manager to run a SELECT query
with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
