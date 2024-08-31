# ベースイメージ
FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係のコピーとインストール
COPY requirements.txt .
RUN pip install -r requirements.txt
