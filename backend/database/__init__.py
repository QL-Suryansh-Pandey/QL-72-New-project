import mysql.connector
from mysql.connector import Error
import os

# Configuration constants (read from environment variables)
DB_HOST = os.environ.get('MYSQL_HOST')
DB_PORT = os.environ.get('MYSQL_PORT', '3306')
DB_USER = os.environ.get('MYSQL_USERNAME')
DB_PASSWORD = os.environ.get('MYSQL_PASSWORD')

# NOTE: We use the database name provided in the environment variables for connection.
# The setup script (database_setup.sql) handles the creation of the specific database.
# For the connection layer, we assume the database exists or we handle connection failure.

def get_db_connection():
    """Establishes and returns a connection object to MySQL."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASSWORD,
            # We connect without specifying a database initially for setup/connection testing
            # or we specify a known database if we are past the setup phase.
            # For initial connection test, we might connect to the server instance.
            # For this implementation, we rely on the DB being created by the setup script.
            database=os.environ.get('MYSQL_DATABASE')
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        # Re-raise the error to be handled gracefully by the caller
        raise ConnectionError(f"Database connection failed: {e}")
    return connection

# Context manager for connection handling
class DatabaseConnection:
    """A context manager to handle database connections safely."""
    def __enter__(self):
        try:
            self.connection = get_db_connection()
            return self.connection
        except ConnectionError as e:
            # Handle connection failure gracefully by logging/raising
            print(f"[Database Error] Cannot establish connection: {e}")
            # In a real app, you might return None or raise a specific HTTP error
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and self.connection.is_connected():
            self.connection.close()

# Global connection utility (optional, but useful for centralized access)
# This is the primary reusable pattern required.
DB_CONTEXT = DatabaseConnection()
