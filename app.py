from flask import Flask, render_template
from models import init_db
import views

app = Flask(__name__)

def print():
    print("Hello World")

