from flask import Flask, render_template
from models import init_db
import views

app = Flask(__name__)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)