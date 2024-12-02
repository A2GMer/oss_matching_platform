import requests
from flask import render_template, redirect, url_for
from app import app, db
from app.models import Repository

# GitHub APIからリポジトリ情報を取得し保存
@app.route('/fetch')
def fetch_repos():
    username = "A2GMer"  # GitHubユーザー名
    # headers = {"Authorization": "token your_github_personal_access_token"}  # 認証トークンを使用（オプション）
    # response = requests.get(f'https://api.github.com/users/{username}/repos', headers=headers)
    response = requests.get(f'https://api.github.com/users/{username}/repos')

    if response.status_code == 200:  # 正常にデータを取得できた場合
        repos = response.json()
        for repo in repos:
            if not repo.get('private', False):  # 非公開リポジトリを除外
                if not Repository.query.filter_by(name=repo['name']).first():
                    new_repo = Repository(
                        name=repo['name'],
                        description=repo.get('description'),
                        url=repo['html_url'],
                        stars=repo.get('stargazers_count', 0),
                        forks=repo.get('forks_count', 0)
                    )
                    db.session.add(new_repo)
        db.session.commit()
        return redirect(url_for('index'))  # トップページにリダイレクト
    else:
        return f"Failed to fetch repositories: {response.status_code}"


# トップページでリポジトリ一覧を表示
@app.route('/')
def index():
    # fetch_repos()  # データベース更新
    repos = Repository.query.all()  # 全リポジトリ情報を取得
    return render_template('index.html', repos=repos)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # templates/dashboard.htmlを返す