from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('base.html')  # templates/index.htmlを返す

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # templates/dashboard.htmlを返す
