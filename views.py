from flask import render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash
from sqlite3 import IntegrityError
from forms import ComplaintForm, RegisterForm, UserRegistrationForm, AdminRegistrationForm

# Home page
def index():
    return render_template('index.html')

# Users page
def users():
    form = UserRegistrationForm()
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    users_data = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users_data, form=form)

# Admins page
def admins():
    form = AdminRegistrationForm()
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Admins')
    admins_data = cursor.fetchall()
    conn.close()
    return render_template('admins.html', admins=admins_data, form=form)

# Route to register new users
def register_user():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password_hash = generate_password_hash(password)

        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Users (username, email, password_hash, role, name, contact_number) VALUES (?, ?, ?, ?, ?, ?)',
                           (username, email, password_hash, form.role.data, form.name.data, form.contact_number.data))
            conn.commit()
            flash('User registered successfully!', 'success')
            return redirect(url_for('index'))
        except IntegrityError:
            flash('User already exists.', 'danger')
            conn.rollback()
        finally:
            conn.close()

    return render_template('register_user.html', form=form)

# Route to register new admins
def register_admin():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password_hash = generate_password_hash(password)

        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Admins (username, email, password_hash, name, phone_number, department) VALUES (?, ?, ?, ?, ?, ?)',
                           (username, email, password_hash, form.name.data, form.phone_number.data, form.department.data))
            conn.commit()
            flash('Admin registered successfully!', 'success')
            return redirect(url_for('index'))
        except IntegrityError:
            flash('Admin already exists.', 'danger')
            conn.rollback()
        finally:
            conn.close()

    return render_template('register_admin.html', form=form)

# Complaints page (GET and POST)
def complaints():
    form = ComplaintForm()
    if request.method == 'POST':
        subject = request.form['subject']
        description = request.form['description']
        severity = request.form['severity']
        
        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO Complaints (subject, description, severity)
        VALUES (?, ?, ?)
        ''', (subject, description, severity))
        conn.commit()
        conn.close()
        
        flash('Your complaint has been submitted successfully.', 'success')
        return redirect(url_for('complaints'))

    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Complaints')

    conn.close()

    return render_template('complaint.html', form=form)

def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password_hash = generate_password_hash(password)

        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()

        try:
            # Insert into the database
            cursor.execute('INSERT INTO User (username, email, password) VALUES (?, ?, ?)', 
                           (username, email, password_hash))
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('index'))

        except IntegrityError:
            # Handle duplicate username or email
            flash('An account with that username or email already exists.', 'danger')
            conn.rollback()

        finally:
            conn.close()

    return render_template('layout.html', form=form)