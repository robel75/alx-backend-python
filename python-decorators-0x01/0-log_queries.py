import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        # Extract the query from either args or kwargs
        query = kwargs.get('query')
        if query is None and len(args) > 0:
            query = args[0]

        print(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)

    return wrapper_log_queries

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
