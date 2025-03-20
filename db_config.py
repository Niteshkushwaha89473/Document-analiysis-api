import psycopg2
from psycopg2 import OperationalError

# Database connection configuration for PostgreSQL
db_config = {
    'dbname': 'document_edit_tool',  # Database name
    'user': 'root',  # Your PostgreSQL username
    'password': 'CIwj7ukheAQKXs6s3hlngInqmvrnc2Ga',  # Your PostgreSQL password
    'host': 'dpg-cvdvof52ng1s73cbi3sg-a',  # Host (localhost or your server IP)
    'port': 5432,  # Default PostgreSQL port
}

def get_db_connection():
    """
    Returns a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(**db_config)
        print('Connection to PostgreSQL database established successfully.')
        return conn
    except OperationalError as e:
        print(f"Error while connecting to PostgreSQL: {e}")
        return None

# Usage example
conn = get_db_connection()
if conn:
    # You can perform your database operations here
    # Don't forget to close the connection when done
    conn.close()
