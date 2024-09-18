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
        CREATE TABLE IF NOT EXISTS Admins (
            adminID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            department TEXT,
            FOREIGN KEY(userID) REFERENCES Users(userID)
        )
    ''')
    
    # Create Complaints table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Complaints (
            complaintID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            description TEXT,
            severity TEXT,
            status TEXT,
            FOREIGN KEY(userID) REFERENCES Users(userID)
        )
    ''')
    
    conn.commit()
    conn.close()
