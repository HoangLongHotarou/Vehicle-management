import uvicorn
from core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from motor.motor_asyncio import AsyncIOMotorClient
from db.database_utils import connect_to_mongo, close_mongo_connection

app = FastAPI(
    openapi_url='/api/v1/license-plate-app/openapi.json',
    docs_url='/api/v1/license-plate-app/docs',
    redoc_url='/api/v1/license-plate-app/redoc',
    title='License plate application',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)

app.add_event_handler('startup',connect_to_mongo)
app.add_event_handler('shutdown',close_mongo_connection)
