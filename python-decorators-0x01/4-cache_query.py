import time
import sqlite3 
import functools

query_cache = {}

# DB connection decorator (copied from previous task)
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper_with_connection(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper_with_connection

# Cache query decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper_cache_query(*args, **kwargs):
        # Get the query string from kwargs or args
        query = kwargs.get("query")
        if query is None and len(args) > 1:
            query = args[1]  # args[0] is conn, args[1] is query

        if query in query_cache:
            print("Returning cached result for query.")
            return query_cache[query]

        result = func(*args, **kwargs)
        query_cache[query] = result
        print("Caching result for query.")
        return result

    return wrapper_cache_query

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
