import sqlite3

class DatabaseConnection:
    def init(self, db_name):
        self.db_name = db_name
        self.conn = None

    def enter(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def exit(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

# Using the context manager to perform a query
with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
