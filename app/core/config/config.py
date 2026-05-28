from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi import FastAPI


class Settings(BaseSettings):
    # Логика для БД
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Логика для JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int
    REFRESH_TOKEN_EXPIRE_SECONDS: int

    APP_NAME: str = "Демо авторизации: session и JWT"
    ACCESS_COOKIE_NAME: str = "access_token"
    RESFRESH_COOKIE_NAME: str = "refresh_token"
    SESSION_COOKIE_SECURE: bool = False
    SESSION_COOKIE_DOMAIN: str | None = None

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=f".env")


settings = Settings()
app = FastAPI()