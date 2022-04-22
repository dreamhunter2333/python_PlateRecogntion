import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    api_id: str
    api_key: str
    api_secret_key: str
    host: str
    port: int
    user: str
    passwd: str
    database: str

    class Config:
        env_file = os.environ.get("ENV_FILE", ".env")


settings = Settings()
