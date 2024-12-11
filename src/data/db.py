import mysql.connector
from mysql.connector import Error
import os


class DB:
    def __init__(self, connection=None):
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.connection = connection

        if not self.connection:
            self.connect()

    def connect(self):
        """Connect to the database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
        except Error as e:
            raise Exception(f"Error connecting to database: {e}")

    def close(self):
        """Disconnect frmo database."""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None):
        """Execute a single query and return results as dictionaries"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            raise Exception(f"Error executing query: {e}")
        finally:
            cursor.close()

    def execute_mutation(self, query, params=None):
        """Execute a query that mutates the database"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
        except Error as e:
            self.connection.rollback()
            raise Exception(f"Error executing non-query: {e}")
        finally:
            cursor.close()

    def execute_transaction(self, queries_with_params):
        """Execute multiple queries within a single transaction."""
        cursor = self.connection.cursor()
        try:
            for query, params in queries_with_params:
                cursor.execute(query, params)
            self.connection.commit()
        except Error as e:
            self.connection.rollback()
            raise Exception(f"Error executing transaction: {e}")
        finally:
            cursor.close()
