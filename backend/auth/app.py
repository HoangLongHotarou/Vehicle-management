import cloudinary
import uvicorn
from api.endpoints import router as api_router
from core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database_utils import connect_to_mongo, close_mongo_connect


cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET
)


app = FastAPI(
    openapi_url='/api/v1/auth/openapi.json',
    docs_url='/api/v1/auth/docs',
    redoc_url='/api/v1/auth/redoc',
    title='Authenticate',
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
app.add_event_handler('shutdown',close_mongo_connect)

app.include_router(api_router)

def start():
    uvicorn.run(
        'app:app',
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
        log_level='info'
    )