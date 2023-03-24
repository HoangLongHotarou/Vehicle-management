from core.celery import celery
from api.controllers.controller import aviFaceController
import asyncio
import base64
from db.database_utils import connect_to_mongo
import cloudinary
from core.config import settings

asyncio.run(connect_to_mongo())

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET
)

try:
    loop = asyncio.get_event_loop()
except RuntimeError as e:
    if str(e).startswith('There is no current event loop in thread'):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    else:
        raise

@celery.task()
def add_avi(video_bytes,username):
    loop.run_until_complete(
        aviFaceController.add_avi(bytes.fromhex(video_bytes), username)
    )
    return "OK"

@celery.task()
def add(a,b):
    print(a+b)
    return a+b