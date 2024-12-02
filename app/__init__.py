from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # MySQLの設定を適宜反映
db = SQLAlchemy(app)

from app import routes  # 必要なルートをインポート
from flask_migrate import Migrate

migrate = Migrate(app, db)
