from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./lighthouse_cards.db"
    SECRET_KEY: str = "change-this-secret-key-in-production-use-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24時間

    model_config = {"env_file": ".env"}


settings = Settings()
