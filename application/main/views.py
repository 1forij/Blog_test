from . import main_blue
from flask import render_template

@main_blue.route('/')
def index():
    return render_template('index.html')