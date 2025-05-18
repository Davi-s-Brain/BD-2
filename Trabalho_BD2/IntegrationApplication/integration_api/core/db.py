import sqlite3

DB_NAME = "local.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        """)
        conn.commit()

def get_connection():
    return sqlite3.connect(DB_NAME)
