from app import db

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # リポジトリ名
    description = db.Column(db.Text, nullable=True)   # 説明
    url = db.Column(db.String(255), nullable=False)   # URL
