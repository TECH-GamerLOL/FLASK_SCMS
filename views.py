from flask import render_template, request, redirect, url_for
import sqlite3

# Index (home) page
def index():
    return render_template('index.html')

# Users page
def users():
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    users_data = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users_data)

# Admins page
def admins():
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Admins')
    admins_data = cursor.fetchall()
    conn.close()
    return render_template('admins.html', admins=admins_data)

# Complaints page (GET and POST)
def complaints():
    if request.method == 'POST':
        user_id = request.form['user_id']
        description = request.form['description']
        severity = request.form['severity']
        
        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Complaints (user_id, description, severity) VALUES (?, ?, ?)', (user_id, description, severity))
        conn.commit()
        conn.close()
        return redirect(url_for('complaints'))

    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Complaints')
    complaints_data = cursor.fetchall()
    conn.close()
    return render_template('complaints.html', complaints=complaints_data)
