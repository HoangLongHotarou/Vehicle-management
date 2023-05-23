from .database import db, AsyncIOMotorClient
from core.config import settings

async def connect_to_mongo():
    db.mongodb_client = AsyncIOMotorClient(
        # 'mongodb://mongo1:27017/?replicaSet=rs0&directConnection=true'
        settings.DB_URL
    )
    db.mongodb = db.mongodb_client[settings.DB_NAME]

async def close_mongo_connection():
    db.mongodb_client.close()