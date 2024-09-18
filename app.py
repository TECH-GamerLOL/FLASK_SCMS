from flask import Flask
from models import init_db
import views

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'

# Initialize database
init_db()

if __name__ == '__main__':
    app.run(debug=True)
