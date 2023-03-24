from motor.motor_asyncio import AsyncIOMotorClient

class BaseDatabase():
    mongodb_client: AsyncIOMotorClient
    mongodb: any = None

db = BaseDatabase()

async def get_database()->BaseDatabase:
    return db