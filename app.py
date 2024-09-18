from flask import Flask
from models import init_db
import views

# Initialize the Flask app
app = Flask(__name__)

# Secret key for form submissions
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database
init_db()

# Register routes from views.py
app.add_url_rule('/', 'index', views.index)  # Change 'home' to 'index'
app.add_url_rule('/users', 'users', views.users)
app.add_url_rule('/admins', 'admins', views.admins)
app.add_url_rule('/complaints', 'complaints', views.complaints, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
