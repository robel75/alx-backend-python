import mysql.connector
import csv
import uuid

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="your_password"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
        """)
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']
                cursor.execute("""
                SELECT * FROM user_data WHERE email = %s;
                """, (email,))
                exists = cursor.fetchone()
                if not exists:
                    cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                    """, (user_id, name, email, age))
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}")
