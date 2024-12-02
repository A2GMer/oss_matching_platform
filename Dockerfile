
# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY requirements.txt requirements.txt
COPY . .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flaskアプリを実行
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
