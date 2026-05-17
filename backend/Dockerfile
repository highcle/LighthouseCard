FROM python:3.12-slim

WORKDIR /app

# 依存ライブラリをインストール（レイヤーキャッシュ活用）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリコードをコピー
COPY app/ app/
COPY seed_data.py .

# DBデータ永続化用ディレクトリ
RUN mkdir -p /data

EXPOSE 8000

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
