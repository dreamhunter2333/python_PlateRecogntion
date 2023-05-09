import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    api_id: str = "15777797"
    api_key: str = "xkQmQk08d7pTP56LqXhqpUbm"
    api_secret_key: str = "bzgSQwTy6WTkXczLlYPfOwu2OQZQ8CEg"
    host: str = "localhost"
    port: int = 3306
    dbuser: str = "python"
    passwd: str = "Python12345@"
    database: str = "chepai"

    class Config:
        env_file = os.environ.get("ENV_FILE", ".env")


settings = Settings()
