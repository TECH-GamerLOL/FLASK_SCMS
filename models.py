import sqlite3

DB_NAME = 'SCMS.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create Admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            adminID INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            department TEXT,
            FOREIGN KEY(user_id) REFERENCES Users(user_id)
        )
    ''')
    
    # Create Complaints table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Complaints (
            complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            description TEXT,
            severity TEXT,
            status TEXT,
            FOREIGN KEY(user_id) REFERENCES Users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()
