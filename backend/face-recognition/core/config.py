import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(dotenv_path='../../env/face-recognition.env')


class CommonSettings(BaseSettings):
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000

class ConstValue(BaseSettings):
    MAX_ELEMENTS = 100000

class DatabaseSettings(BaseSettings):
    DB_URL: str = os.environ.get('MONGODB_URL', 'mongodb+srv://dbRon:Long12345@cluster0.w09ru.mongodb.net/test')
    # DB_URL: str = os.environ.get('mongodb://host.docker.internal:27017/?replicaSet=rs0&directConnection=true')
    DB_NAME: str = os.environ.get('MONGODB_NAME', 'face_recognition_db')


class CloudinarySettings(BaseSettings):
    CLOUD_NAME: str = os.environ.get('CLOUD_NAME', 'dlu')
    API_KEY: str = os.environ.get('API_KEY', '471522412694188')
    API_SECRET: str = os.environ.get(
        'API_SECRET', 'aQAwuL0JbMk0zjnCdcEAco1a6M0')
    STORE: str = 'videos/trains'


class RedisSettings(BaseSettings):
    REDIS_URL: str = os.environ.get('REDIS_URL', 'redis://redis:6379')


class Settings(
    CommonSettings,
    ServerSettings,
    DatabaseSettings,
    CloudinarySettings,
    RedisSettings,
    ConstValue
):
    pass


settings = Settings()
