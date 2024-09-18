from flask import render_template, request, redirect, url_for
import sqlite3

# Index (home) page
def index():
    return render_template('index.html')

# Users page
def users():
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User')
    users_data = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users_data)

# Admins page
def admins():
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Admin')
    admins_data = cursor.fetchall()
    conn.close()
    return render_template('admins.html', admins=admins_data)

# Complaints page (GET and POST)
def complaints():
    if request.method == 'POST':
        student_id = request.form['StudentID']
        description = request.form['description']
        status = request.form['status']
        
        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Complaints (student_id, description, status) VALUES (?, ?, ?)', (student_id, description, status))
        conn.commit()
        conn.close()
        return redirect(url_for('complaints'))

    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Complaints')
    complaints_data = cursor.fetchall()
    conn.close()
    return render_template('complaint.html', complaints=complaints_data)
