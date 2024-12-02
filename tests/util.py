import os
import mysql.connector


def create_database(test_db_name: str):
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = int(os.getenv("DB_PORT", 3306))
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    connection = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
    )

    cursor = connection.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {test_db_name}")
    connection.commit()

    connection.database = test_db_name
    cursor.close()

    return connection


def drop_database(test_db_name: str, connection):
    """Delete the test database to start fresh for the next test."""
    cursor = connection.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
    connection.commit()
    cursor.close()
    connection.close()


def execute_all(statements, connection):
    cursor = connection.cursor()
    try:
        # split at ';' characters and then take line by line
        statements = statements.split(";")
        for statement in statements:
            statement = statement.strip()
            if statement and statement not in [
                "START TRANSACTION",
                "COMMIT",
                "ROLLBACK",
            ]:
                cursor.execute(statement)

        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error during migration: {e}")
    finally:
        cursor.close()


def migrate(connection):
    # Initialise the database
    with open("migrations/1_init.sql", "r") as file:
        statements = file.read()
        execute_all(statements, connection)

    # Load dummy data
    with open("migrations/2_dummy_data.sql", "r") as file:
        statements = file.read()
        execute_all(statements, connection)
