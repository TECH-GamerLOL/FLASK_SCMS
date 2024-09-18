from flask import render_template, redirect, url_for, request
from app import app
from models import DB_NAME
import sqlite3
from forms import ComplaintForm

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/users')
def users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/admins')
def admins():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Admins")
    admins = cursor.fetchall()
    conn.close()
    return render_template('admins.html', admins=admins)

@app.route('/complaints', methods=['GET', 'POST'])
def complaints():
    form = ComplaintForm()
    if form.validate_on_submit():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Complaints (user_id, subject, description, severity, status)
            VALUES (?, ?, ?, ?, ?)''', (1, form.subject.data, form.description.data, form.severity.data, 'pending'))
        conn.commit()
        conn.close()
        return redirect(url_for('complaints'))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Complaints")
    complaints = cursor.fetchall()
    conn.close()
    return render_template('complaints.html', complaints=complaints, form=form)
