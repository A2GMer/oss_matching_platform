from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

import os

# app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # MySQLの設定を適宜反映
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import secrets
app.secret_key = secrets.token_hex(32)

load_dotenv()  # .envファイルを読み込む
app.config['GITHUB_CLIENT_ID'] = os.getenv('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.getenv('GITHUB_CLIENT_SECRET')
app.config['GITHUB_REDIRECT_URI'] = 'http://localhost:5000/callback'

from app import routes
