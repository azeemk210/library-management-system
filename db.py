import psycopg
from psycopg.rows import dict_row


DATABASE_URL = {"host": "hostname", "dbname": "dbname", "user": "user", "password": "password"}

def get_db_connection():
    conn = psycopg.connect(**DATABASE_URL, row_factory=dict_row)
    return conn, conn.cursor()

