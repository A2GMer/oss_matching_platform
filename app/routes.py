from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('index.html')  # templates/index.htmlを返す

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # templates/dashboard.htmlを返す

@app.route('/about')
def about():
    return "<h1>About Page</h1>"  # 簡易的なHTMLを直接返す
