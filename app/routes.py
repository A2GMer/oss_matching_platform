from flask import render_template
from app import app, db

@app.route('/')
def index():
    repos = Repository.query.all()  # 全リポジトリ情報を取得
    return render_template('index.html', repos=repos)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # templates/dashboard.htmlを返す



# サンプルデータの登録
from app.models import Repository

@app.route('/add-sample')
def add_sample():
    sample_repos = [
        Repository(name="Flask", description="A lightweight WSGI web application framework.", url="https://flask.palletsprojects.com/"),
        Repository(name="Django", description="The web framework for perfectionists with deadlines.", url="https://www.djangoproject.com/"),
        Repository(name="SQLAlchemy", description="SQL Toolkit and Object Relational Mapper.", url="https://www.sqlalchemy.org/"),
    ]
    db.session.add_all(sample_repos)
    db.session.commit()
    return "Sample data added!"
