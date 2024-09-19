from flask import render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import check_password_hash
from sqlite3 import IntegrityError
from forms import ComplaintForm, RegisterForm, LoginForm, AdminComplaintForm, ResetPasswordForm, ProfileForm
from email_validator import validate_email, EmailNotValidError
import app



# Home page
def index():
    return render_template('index.html')

def admins():
    if 'userID' not in session or get_user_role(session['userID']) != 'admin':
        flash('You must be logged in as an admin to view complaints.', 'warning')
        return redirect(url_for('login'))

    form = AdminComplaintForm()
    
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()

    # Handle status update
    if request.method == 'POST' and form.validate_on_submit():
        complaint_id = form.complaint_id.data
        new_status = form.status.data
        
        cursor.execute('UPDATE Complaints SET status = ? WHERE id = ?', (new_status, complaint_id))
        conn.commit()
        flash('Complaint status updated successfully!', 'success')

    # Retrieve all complaints
    cursor.execute('SELECT * FROM Complaints')
    complaints_data = cursor.fetchall()
    conn.close()

    return render_template('admin_complaints.html', complaints=complaints_data, form=form)

def get_user_role(user_id):
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM Users WHERE userID = ?', (user_id,))
    role = cursor.fetchone()[0]
    conn.close()
    return role

def users():
    if 'userID' not in session:
        flash('You must be logged in to view users.', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    conn.close()

    return render_template('users.html', users=users)


def complaints():
    # Check if user is logged in
    if 'userID' not in session:
        flash('You must be logged in to submit a complaint.', 'warning')
        return redirect(url_for('login'))

    form = ComplaintForm()

    if form.validate_on_submit():
        subject = form.subject.data
        description = form.description.data
        severity = form.severity.data
        user_id = session['userID']

        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()

        try:
            # Insert the complaint into the database
            cursor.execute('INSERT INTO Complaints (subject, description, severity, status, userID) VALUES (?, ?, ?, ?, ?)', 
                           (subject, description, severity, 'Pending', user_id))
            conn.commit()
            flash('Complaint submitted successfully!', 'success')
        except Exception as e:
            flash('Error submitting complaint.', 'danger')
            conn.rollback()
        finally:
            conn.close()
        
        return redirect(url_for('index'))

    # Optionally, you can retrieve and display all complaints here if needed
    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Complaints')
    complaints_data = cursor.fetchall()
    conn.close()
    
    return render_template('complaint.html', complaints=complaints_data, form=form)

def register():
    form = RegisterForm()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  # Assuming form field is 'password'
        
        print(f"Username: {username}, Email: {email}, Password: {password}")  # Debug print
        
        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        
        try:
            # Check if the username already exists
            cursor.execute('SELECT COUNT(*) FROM Users WHERE username = ?', (username,))
            username_exists = cursor.fetchone()[0]
            print(f"Username exists: {username_exists}")  # Debug print
            
            if username_exists:
                flash('An account with that username already exists.', 'danger')
            else:
                # Insert the new user into the database
                cursor.execute('INSERT INTO Users (username, email, password_hash, role) VALUES (?, ?, ?, ?)', 
                               (username, email, password, 'student'))
                conn.commit()
                flash('Registration successful! You are registered as a student and can now log in.', 'success')
                return redirect(url_for('login'))
        
        except Exception as e:
            print(f"Error: {e}")  # Print detailed error message
            flash('An error occurred during registration. Please try again.', 'danger')
            conn.rollback()
        
        finally:
            conn.close()
    
    return render_template('register.html', form=form)

def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        cursor.execute('SELECT userID, username, password_hash, role FROM Users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            print(user)
            # Extract values from the user tuple
            user_id, db_username, db_password_hash, role = user
            print (f"Password: {db_password_hash}")
            print(f"Password: {password}")  # Debug print
            # Check the password
            if password == db_password_hash:  # No hashing, direct comparison
                print(f"User ID: {user_id}, Username: {db_username}, Password: {db_password_hash}, Role: {role}")  # Debug print
                session['userID'] = user_id  # Store the user's ID in session
                session['username'] = db_username  # Store the username
                session['role'] = role  # Store the user's role
                
                flash('Login successful!', 'success')
                
                # Redirect based on role
                if role == 'admin':
                    print("Admin role detected")  # Debug print
                    return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
                elif role == 'student':
                    print("Student role detected")  # Debug print
                    return redirect(url_for('profile'))  # Redirect to student's profile page
                else:
                    flash('Unknown role assigned to user', 'danger')
                    return redirect(url_for('login'))  # Redirect to login page if role is unknown
            else:
                flash('Invalid username or password', 'danger')
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)

def logout():
    session.clear()  # Clears all session data
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

def profile():

    form = ProfileForm()

    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        
        conn = sqlite3.connect('SCMS.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT password_hash FROM Users WHERE userID = ?', (session['userID'],))
        user = cursor.fetchone()
        
        if user:
            db_password_hash = user[0]
            
            if current_password == db_password_hash:
                # Update the password in the database
                cursor.execute('UPDATE Users SET password_hash = ? WHERE userID = ?', (new_password, session['userID']))
                conn.commit()
                print("Password updated successfully.")  # Debug print
                flash('Password updated successfully.', 'success')
                conn.close()
                return redirect(url_for('profiles'))  # Redirect to homepage after successful update
            else:
                flash('Current password is incorrect.', 'danger')
        else:
            flash('User not found.', 'danger')
        
        conn.close()

    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT username FROM Users WHERE userID = ?', (session['userID'],))
    user_info = cursor.fetchone()
    
    cursor.execute('SELECT subject, description, severity, status FROM Complaints WHERE userID = ?', (session['userID'],))
    complaints = cursor.fetchall()
    
    conn.close()
    
    return render_template('profile.html', form=form, user_info=user_info, complaints=complaints)

def admin_dashboard():
    if 'userID' not in session or session.get('role') != 'admin':
        flash('You must be logged in as an admin to view this page.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('admin_dashboard.html')

def admin_complaints():
    if 'userID' not in session or session.get('role') != 'admin':
        flash('You must be logged in as an admin to view this page.', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT complaintID, subject, description, severity, status FROM Complaints')
    complaints = cursor.fetchall()
    conn.close()

    return render_template('admin_complaints.html', complaints=complaints)


def admin_users():
    if 'userID' not in session or session.get('role') != 'admin':
        flash('You must be logged in as an admin to view this page.', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT userID, username, email FROM Users')
    users = cursor.fetchall()
    conn.close()

    return render_template('admin_users.html', users=users)

def delete_complaint(complaint_id):
    if 'userID' not in session or session.get('role') != 'admin':
        flash('You must be logged in as an admin to perform this action.', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Complaints WHERE complaintID = ?', (complaint_id,))
    conn.commit()
    conn.close()
    flash('Complaint deleted successfully.', 'success')
    return redirect(url_for('admin_complaints'))

def delete_user(user_id):
    if 'userID' not in session or session.get('role') != 'admin':
        flash('You must be logged in as an admin to perform this action.', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('SCMS.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Users WHERE userID = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin_users'))


if __name__ == '__main__':
    app.run(debug=True)