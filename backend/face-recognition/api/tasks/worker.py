from core.celery import celery
from api.controllers.controller import faceRecognitionCtrl
import base64
from db.database_utils import connect_to_mongo,close_mongo_connection
import cloudinary
from core.config import settings
from asgiref.sync import async_to_sync

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET
)

async def processing(video_bytes,username, option, info):
    await connect_to_mongo()
    await faceRecognitionCtrl.train(
        bytes.fromhex(video_bytes), 
        username,
        option,
        info
    )
    await close_mongo_connection()

@celery.task()
def task_train(video_bytes,username, option, info):
    async_to_sync(processing)(video_bytes, username, option, info)

@celery.task()
def add(a,b):
    print(a+b)
    return a+b