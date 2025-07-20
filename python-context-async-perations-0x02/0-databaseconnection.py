import sqlite3

class DatabaseConnection:
    def init(self, db_name):
        """Initialize with the database name"""
        self.db_name = db_name
        self.conn = None

    def enter(self):
        """Open the connection and return it"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def exit(self, exc_type, exc_value, traceback):
        """Close the connection on exit"""
        if self.conn:
            self.conn.close()

# Usage of the context manager
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
