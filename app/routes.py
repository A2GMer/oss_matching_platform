import requests
from flask import redirect, url_for, session, request, render_template
from app import app, db
from app.models import Repository
from app.models import User
from authlib.integrations.flask_client import OAuth
from app.decorators import login_required



@app.route('/mypage')
@login_required
def mypage():
    # GitHub APIを使用してログイン中のユーザーのリポジトリを取得
    token = session.get('github_token')
    if not token:
        return redirect(url_for('login'))

    github_user = session.get('username')  # ユーザー名を取得
    headers = {"Authorization": f"token {token}"}
    response = requests.get(f'https://api.github.com/users/{github_user}/repos', headers=headers)
    if response.status_code != 200:
        return f"Failed to fetch repositories: {response.status_code}"
    
    repos = response.json()  # リポジトリ情報をJSONで取得

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
    return render_template('mypage.html', repos=repos, username=github_user)


# トップページでリポジトリ一覧を表示
@app.route('/')
def index():
    # fetch_repos()  # データベース更新
    repos = Repository.query.all()  # 全リポジトリ情報を取得
    return render_template('index.html', repos=repos)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # templates/dashboard.htmlを返す


# OAuth設定
oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id=app.config['GITHUB_CLIENT_ID'],
    client_secret=app.config['GITHUB_CLIENT_SECRET'],
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


# ログインルート
@app.route('/login')
def login():
    return github.authorize_redirect(url_for('authorize', _external=True))


# コールバックルート
@app.route('/callback')
def authorize():
    token = github.authorize_access_token()
    resp = github.get('user')
    profile = resp.json()

    # GitHubユーザーをデータベースに保存
    github_id = profile['id']
    username = profile['login']
    email = profile.get('email')

    user = User.query.filter_by(github_id=github_id).first()
    if not user:
        user = User(username=username, github_id=github_id, email=email)
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user.id
    session['username'] = username
    session['github_token'] = token['access_token']
    return redirect(url_for('index'))


# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))