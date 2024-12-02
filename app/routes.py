import requests
from flask import redirect, url_for, session, request, render_template
from app import app, db
from app.models import Repository
from app.models import User
from app.models import Language
from app.models import Framework
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
    user_id = session['user_id']
    languages = Language.query.filter_by(user_id=user_id).all()
    frameworks = Framework.query.filter_by(user_id=user_id).all()

    headers = {"Authorization": f"token {token}"}
    response = requests.get(f'https://api.github.com/users/{github_user}/repos', headers=headers)
    if response.status_code != 200:
        return f"Failed to fetch repositories: {response.status_code}"
    
    repos = response.json()  # リポジトリ情報をJSONで取得

    for repo in repos:
        if not repo.get('private', False):  # 非公開リポジトリを除外
            if not Repository.query.filter_by(name=repo['name']).first():
                # GitHub APIから使用言語を取得
                res = requests.get(f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/languages", headers=headers)
                languages = res.json() if res.status_code == 200 else {}
            
                # 言語をカンマ区切りの文字列として保存
                languages_str = ', '.join(languages.keys())

                new_repo = Repository(
                    name=repo['name'],
                    description=repo.get('description'),
                    url=repo['html_url'],
                    stars=repo.get('stargazers_count', 0),
                    forks=repo.get('forks_count', 0),
                    languages=languages_str  # 使用言語を保存
                )
                db.session.add(new_repo)
    db.session.commit()
    return render_template('mypage.html', repos=repos, username=github_user, languages=languages, frameworks=frameworks)


# トップページでリポジトリ一覧を表示
@app.route('/')
def index():
    # 全リポジトリを取得（共通処理）
    repos = Repository.query.all()  # 全リポジトリ情報を取得

    if 'user_id' not in session:
        recommended_repos = []  # 非ログイン時はレコメンドを空に
        return render_template('index.html', recommended_repos=recommended_repos, repos=repos)

    user_id = session['user_id']
    # 最も経験年数が長い言語とフレームワークを取得
    top_language = db.session.query(Language).filter_by(user_id=user_id).order_by(Language.experience_years.desc()).first()
    top_framework = db.session.query(Framework).filter_by(user_id=user_id).order_by(Framework.experience_years.desc()).first()

    # 比較して最長のものを選択
    if top_language and (not top_framework or top_language.experience_years >= top_framework.experience_years):
        top_skill = top_language.language_name
    elif top_framework:
        top_skill = top_framework.framework_name
    else:
        top_skill = None

    # リポジトリをレコメンド
    recommended_repos = []
    if top_skill:
        recommended_repos = db.session.query(Repository).filter(
            db.or_(
                Repository.languages.ilike(f"%{top_skill}%"),
                Repository.frameworks.ilike(f"%{top_skill}%")
            )
        ).all()

    return render_template('index.html', recommended_repos=recommended_repos, repos=repos)



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

# 言語の登録
@app.route('/add_language', methods=['POST'])
@login_required
def add_language():
    user_id = session['user_id']
    language_name = request.form['language_name']
    experience_years = int(request.form['experience_years'])

    new_language = Language(user_id=user_id, language_name=language_name, experience_years=experience_years)
    db.session.add(new_language)
    db.session.commit()
    return redirect(url_for('mypage'))

# フレームワークの登録
@app.route('/add_framework', methods=['POST'])
@login_required
def add_framework():
    user_id = session['user_id']
    framework_name = request.form['framework_name']
    experience_years = int(request.form['experience_years'])

    new_framework = Framework(user_id=user_id, framework_name=framework_name, experience_years=experience_years)
    db.session.add(new_framework)
    db.session.commit()
    return redirect(url_for('mypage'))

# 言語の削除
@app.route('/delete_language', methods=['POST'])
@login_required
def delete_language():
    language_id = request.form['language_id']
    language = Language.query.get(language_id)
    db.session.delete(language)
    db.session.commit()
    return redirect(url_for('mypage'))

# フレームワークの削除
@app.route('/delete_framework', methods=['POST'])
@login_required
def delete_framework():
    framework_id = request.form['framework_id']
    framework = Framework.query.get(framework_id)
    db.session.delete(framework)
    db.session.commit()
    return redirect(url_for('mypage'))

