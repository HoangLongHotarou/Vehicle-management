import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(dotenv_path='../../env/license-plate-app.env')


class CommonSettings(BaseSettings):
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = os.environ.get('MONGODB_URL')
    DB_NAME: str = os.environ.get('MONGODB_NAME')


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str = os.environ.get(
        'JWT_SECRET_KEY', 'df5b1fa03b8329d36348f3208923181f')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PATH_KEY: str = 'c20c4a219481f901'


class RedisSettings(BaseSettings):
    REDIS_BROKER: str = os.environ.get('REDIS_URL')
    REDIS_BACKEND: str = os.environ.get(
        'REDIS_URL', 'redis://localhost:6379/0'
    )


class Settings(CommonSettings, ServerSettings, DatabaseSettings, JWTSettings, RedisSettings):
    pass


settings = Settings()
