from flask import render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from sqlite3 import IntegrityError
from forms import ComplaintForm, RegisterForm, UserRegistrationForm, LoginForm, AdminRegistrationForm
from email_validator import validate_email, EmailNotValidError
import app


# Home page
def index():
    return render_template('index.html')

def admins():
    form = AdminRegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password_hash = generate_password_hash(password)
        
        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        
        try:
            # Insert the admin into the database
            cursor.execute('INSERT INTO Admins (username, email, password_hash) VALUES (?, ?, ?)', 
                           (username, email, password_hash))
            conn.commit()
            flash('Admin registered successfully!', 'success')
        except IntegrityError:
            flash('An account with that username or email already exists.', 'danger')
            conn.rollback()
        finally:
            conn.close()
        return redirect(url_for('admins'))

    # Retrieve all admins
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Admins')
    admins_data = cursor.fetchall()
    conn.close()
    
    return render_template('admins.html', admins=admins_data, form=form)

def users():
    form = UserRegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password_hash = generate_password_hash(password)
        
        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        
        try:
            # Insert the user into the database
            cursor.execute('INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)', 
                           (username, email, password_hash))
            conn.commit()
            flash('User registered successfully!', 'success')
        except IntegrityError:
            flash('An account with that username or email already exists.', 'danger')
            conn.rollback()
        finally:
            conn.close()
        return redirect(url_for('users'))

    # Retrieve all users
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    users_data = cursor.fetchall()
    conn.close()
    
    return render_template('users.html', users=users_data, form=form, register_form=form)


# Complaints page
def complaints():
    form = ComplaintForm()
    
    if form.validate_on_submit():
        subject = form.subject.data
        description = form.description.data
        severity = form.severity.data
        
        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        
        try:
            # Insert the complaint into the database
            cursor.execute('INSERT INTO Complaints (subject, description, severity, status) VALUES (?, ?, ?, ?)', 
                           (subject, description, severity, 'Pending'))
            conn.commit()
            flash('Complaint submitted successfully!', 'success')
        except Exception as e:
            flash('Error submitting complaint.', 'danger')
            conn.rollback()
        finally:
            conn.close()
        return redirect(url_for('index'))

    # Retrieve all complaints
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Complaints')
    complaints_data = cursor.fetchall()
    conn.close()
    
    return render_template('complaint.html', complaints=complaints_data, form=form)

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
            cursor.execute('INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)', 
                           (username, email, password_hash))
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            flash('An account with that username or email already exists.', 'danger')
            conn.rollback()
        finally:
            conn.close()
    return render_template('register.html', form=form)

def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT password_hash FROM Users WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result and check_password_hash(result[0], password):
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to a protected page or dashboard
        else:
            flash('Invalid username or password.', 'danger')
        conn.close()
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)