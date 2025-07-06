from seed import connect_to_prodev

def stream_user_ages():
    """Generator that yields user ages one by one from the database."""
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row[0]
    connection.close()


def compute_average_age():
    """Computes the average age using a generator without loading all data into memory."""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        print(f"Average age of users: {total_age / count:.2f}")
    else:
        print("No users found.")

if name == "main":
    compute_average_age()
