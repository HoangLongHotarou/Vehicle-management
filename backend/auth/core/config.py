import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(dotenv_path='../../env/auth.env')


class CommonSettings(BaseSettings):
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = os.environ.get('MONGODB_URL')
    DB_NAME: str = os.environ.get('MONGODB_NAME')


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*30
    PATH_KEY: str = 'c20c4a219481f901'


class OTPSettings(BaseSettings):
    ACCESS_OTP_EXPIRE_SECONDS: int = 120


class EmailEnvSettings(BaseSettings):
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD')
    MAIL_FROM: str = os.environ.get('MAIL_FROM')
    MAIL_PORT: int = 587
    MAIL_FROM_NAME: str = 'Quản lý phương tiện DLU'
    MAIL_SERVER: str = 'smtp.gmail.com'


class CloudinarySettings(BaseSettings):
    CLOUD_NAME:str = os.environ.get('CLOUD_NAME')
    API_KEY:str = os.environ.get('API_KEY')
    API_SECRET:str = os.environ.get('API_SECRET')
    STORE:str = 'images/avatars'


class Settings(
        CommonSettings,
        ServerSettings,
        DatabaseSettings,
        JWTSettings,
        OTPSettings,
        EmailEnvSettings,
        CloudinarySettings):
    pass


settings = Settings()
