#!/bin/sh
set -e

# 初回起動時にシードデータを投入
python seed_data.py

# APIサーバー起動
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
