import mysql.connector
from mysql.connector import Error

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'pC8vEasaFu4nRqgacKkkSOWq8JAuTyJb',
    'host': 'dpg-cvdvjk7noe9s73ej9ro0-a',
    'database': 'document_edit_tool',
}

def get_db_connection():
    """
    Returns a connection to the MySQL database.
    """
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print('Connection to MySQL database established successfully.')
            return conn
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
