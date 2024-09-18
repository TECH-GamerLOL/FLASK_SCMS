# app.py

from flask import Flask
import views
from models import init_db  # Ensure init_db is imported correctly

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

if __name__ == '__main__':
    app.run(debug=True)
