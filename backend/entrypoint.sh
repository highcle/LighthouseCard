#!/bin/sh
set -e

python seed_data.py

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8080}"
