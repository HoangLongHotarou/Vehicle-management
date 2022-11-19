from .database import db, AsyncIOMotorClient
from core.config import settings

async def connect_to_mongo():
    db.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    db.mongodb = db.mongodb_client[settings.DB_NAME]

async def close_mongo_connect():
    db.mongodb_client.close()