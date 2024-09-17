import sqlite3

Database = 'SCMS.db'

def get_db():
    conn = sqlite3.connect(Database)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            studentid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()