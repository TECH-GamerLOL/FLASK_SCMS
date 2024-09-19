# app.py

from flask import Flask, session
import views
from models import init_db  # Ensure init_db is imported correctly

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # This is needed to sign the session cookies


# Initialize the Flask app
app = Flask(__name__)

# Secret key for form submissions
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database
init_db()

# Register routes using decorators
@app.route('/')
def index():
    return views.index()

@app.route('/users')
def users():
    return views.users()

@app.route('/admins')
def admins():
    return views.admins()

@app.route('/complaints', methods=['GET', 'POST'])
def complaints():
    return views.complaints()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return views.register()

@app.route('/login', methods=['GET','POST'] )
def login():
    return views.login()

@app.route('/logout')
def logout():
    return views.logout()

@app.route('/profile')
def profile():
    return views.profile()

@app.route('/admin_dashboard')
def admin_dashboard():
    return views.admin_dashboard()

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return views.reset_password()


@app.route('/delete_complaint/<int:complaint_id>', methods=['POST'])
def delete_complaint(complaint_id):
    return views.delete_complaint(complaint_id)

@app.route('/admin_users', methods=['GET'])
def admin_users():
    return views.admin_users()

@app.route('/admin_complaints', methods=['GET'])
def admin_complaints():
    return views.admin_complaints()

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    return views.delete_user(user_id)

if __name__ == '__main__':
    app.run(debug=True)
