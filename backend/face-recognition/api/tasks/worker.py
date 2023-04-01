from core.celery import celery
from api.controllers.controller import faceRecognitionController
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

async def processing(video_bytes,username):
    await connect_to_mongo()
    await faceRecognitionController.train(
        bytes.fromhex(video_bytes), 
        username
    )
    await close_mongo_connection()

@celery.task()
def task_train(video_bytes,username):
    async_to_sync(processing)(video_bytes, username)

@celery.task()
def add(a,b):
    print(a+b)
    return a+b