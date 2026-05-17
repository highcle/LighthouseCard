#!/bin/bash
# 灯台カード収集管理アプリ 起動スクリプト

set -e

NODE="/home/highcle/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/node"
NODE_DIR=$(dirname "$NODE")
NPM_CLI="/tmp/package/index.js"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# npmが/tmpにない場合はダウンロード
if [ ! -f "$NPM_CLI" ]; then
  echo "npmをダウンロード中..."
  curl -sL https://registry.npmjs.org/npm/-/npm-10.9.2.tgz -o /tmp/npm.tgz
  tar xzf /tmp/npm.tgz -C /tmp/
fi

export PATH="$NODE_DIR:$PATH"

echo "=== バックエンド起動 (port 8000) ==="
cd "$SCRIPT_DIR/backend"
./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo "=== フロントエンド起動 (port 5173) ==="
cd "$SCRIPT_DIR/frontend"
"$NODE" "$NPM_CLI" run dev &
FRONTEND_PID=$!

echo ""
echo "起動完了！"
echo "  フロントエンド: http://localhost:5173"
echo "  バックエンドAPI: http://localhost:8000"
echo "  API ドキュメント: http://localhost:8000/docs"
echo ""
echo "停止するには Ctrl+C を押してください"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
