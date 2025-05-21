import sqlite3

DB_NAME = "locals.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        name TEXT NOT NULL PRIMARY KEY,
        description TEXT,
        quantity INTEGER NOT NULL,
        value INTEGER NOT NULL
    )
""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionario (
            Id_func INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_func TEXT NOT NULL,
            CPF TEXT NOT NULL UNIQUE,
            Data_nasc_func TEXT NOT NULL,
            Cargo TEXT NOT NULL,
            Salario REAL NOT NULL,
            Data_admissao TEXT NOT NULL,
            Turno TEXT NOT NULL,
            Tipo_de_contrato TEXT NOT NULL,
            Status_func TEXT NOT NULL,
            Id_franquia INTEGER
        )
        """)

        conn.commit()

def get_connection():
    return sqlite3.connect(DB_NAME)