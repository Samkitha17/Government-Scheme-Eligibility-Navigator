import sqlite3

DATABASE = "schemes.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            min_age INTEGER,
            max_age INTEGER,
            max_income INTEGER,
            occupation TEXT,
            social_category TEXT,
            benefit TEXT,
            documents TEXT
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")