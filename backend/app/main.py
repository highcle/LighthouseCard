import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import user, lighthouse, user_card  # noqa: F401 — モデル登録
from .routers import auth, lighthouses, cards

Base.metadata.create_all(bind=engine)

app = FastAPI(title="灯台カード収集管理 API", version="1.0.0")

_default_origins = "http://localhost:5173,http://localhost:3000"
_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", _default_origins).split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(lighthouses.router, prefix="/api/v1")
app.include_router(cards.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "灯台カード収集管理 API"}
