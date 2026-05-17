# 灯台カード収集帳

海上保安庁が管理する **灯台カードDigital** の収集状況をデジタルで管理するWebアプリです。
現地でQRコードをスキャンするだけで、あなたのコレクションを記録・管理できます。

## 機能

- **ユーザー登録・ログイン** — メールアドレス・パスワードで登録、JWT認証
- **QRコードスキャン** — 現地の灯台に掲示されたQRコードをカメラで読み取り、自動で灯台を特定して収集登録
- **手動登録** — QRが読めない場合は灯台名で検索して登録
- **コレクション管理** — 収集済みカードの一覧表示・メモ追加・削除
- **ダッシュボード** — 収集枚数・達成率・地域別進捗グラフ
- **全国地図** — 全灯台をマップ表示（収集済み:緑 / 未収集:グレー）
- **灯台一覧・詳細** — 地域・都道府県フィルタ、灯台ごとの詳細情報

## 技術スタック

| 層 | 技術 |
|---|---|
| バックエンド | Python 3.12 + FastAPI + SQLAlchemy 2.x |
| データベース | SQLite（開発） / PostgreSQL対応可 |
| 認証 | JWT (python-jose) + bcrypt |
| フロントエンド | React 18 + TypeScript + Vite |
| スタイリング | Tailwind CSS |
| QRスキャン | html5-qrcode |
| 地図 | React Leaflet |
| 状態管理 | Zustand |
| Webサーバー（本番） | nginx |

## ディレクトリ構成

```
LighthouseCard/
├── backend/
│   ├── app/
│   │   ├── core/          # 設定・JWT・パスワードハッシュ
│   │   ├── models/        # SQLAlchemyモデル（users, lighthouses, user_cards）
│   │   ├── routers/       # APIルーター（auth, lighthouses, cards）
│   │   ├── schemas/       # Pydanticスキーマ
│   │   ├── services/      # QRコードURL解析ロジック
│   │   ├── database.py
│   │   └── main.py
│   ├── seed_data.py       # 全国28灯台の初期データ投入スクリプト
│   ├── entrypoint.sh
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/           # axiosクライアント・各APIモジュール
│   │   ├── components/    # 共通コンポーネント
│   │   ├── pages/         # 各画面
│   │   ├── store/         # Zustand認証ストア
│   │   └── types/         # TypeScript型定義
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml      # 本番用
├── docker-compose.dev.yml  # 開発用（ホットリロード）
├── .env.example
└── 設計書.md
```

## セットアップ

### Docker を使う場合（推奨）

```bash
# 1. 環境変数ファイルを作成
cp .env.example .env

# 2. .env の SECRET_KEY を長いランダム文字列に変更
#    例: openssl rand -hex 32

# 3. 起動（初回はイメージビルドのため数分かかります）
docker compose up -d

# ブラウザで http://localhost を開く
```

> 初回起動時、バックエンドが自動でシードデータ（全国28灯台）を投入します。

### ローカルで直接起動する場合

**バックエンド**

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py             # シードデータ投入
uvicorn app.main:app --reload --port 8000
```

**フロントエンド**

```bash
cd frontend
npm install
npm run dev
```

ブラウザで `http://localhost:5173` を開いてください。

## API ドキュメント

バックエンド起動後、以下のURLで Swagger UI を確認できます。

```
http://localhost:8000/docs
```

### 主要エンドポイント

| メソッド | パス | 説明 |
|---|---|---|
| POST | `/api/v1/auth/register` | ユーザー登録 |
| POST | `/api/v1/auth/login` | ログイン（JWTトークン取得） |
| GET | `/api/v1/auth/me` | 現在のユーザー情報 |
| GET | `/api/v1/lighthouses` | 灯台一覧（検索・フィルタ対応） |
| GET | `/api/v1/lighthouses/{id}` | 灯台詳細 |
| POST | `/api/v1/lighthouses/identify-by-url` | QRコードURLから灯台を特定 |
| GET | `/api/v1/cards` | 自分の収集済みカード一覧 |
| POST | `/api/v1/cards` | カードを収集済みに登録 |
| PATCH | `/api/v1/cards/{lighthouse_id}` | メモを更新 |
| DELETE | `/api/v1/cards/{lighthouse_id}` | 収集記録を削除 |
| GET | `/api/v1/cards/stats` | 収集統計（達成率・地域別） |

## 環境変数

`.env.example` をコピーして `.env` を作成してください。

| 変数名 | 説明 | デフォルト値 |
|---|---|---|
| `SECRET_KEY` | JWT署名用シークレットキー（**本番では必ず変更**） | — |
| `DATABASE_URL` | データベース接続URL | `sqlite:///./lighthouse_cards.db` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWTトークンの有効期限（分） | `1440`（24時間） |

## 開発用コマンド

```bash
# 開発環境をホットリロード付きで起動
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# コンテナを停止
docker compose down

# DBデータも含めて完全リセット
docker compose down -v
```

## シードデータ

全国28灯台のデータが初期投入されます。

| 地域 | 灯台数 |
|---|---|
| 北海道・東北 | 5基 |
| 関東・北陸・東海 | 8基 |
| 近畿・中国・四国 | 9基 |
| 九州・沖縄 | 6基 |

灯台カードの追加は `backend/seed_data.py` の `LIGHTHOUSES` リストに追記し、DBを再作成するだけで対応できます。

## ライセンス

MIT
