from app import db

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # リポジトリ名
    description = db.Column(db.Text, nullable=True)   # 説明
    url = db.Column(db.String(255), nullable=False)   # URL
    stars = db.Column(db.Integer, nullable=True)      # スター数
    forks = db.Column(db.Integer, nullable=True)      # フォーク数

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=True)
