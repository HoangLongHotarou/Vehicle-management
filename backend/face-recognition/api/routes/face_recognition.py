from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks, File
from api.controllers.controller import aviFaceController
import numpy as np
from core.config import settings
from PIL import Image
import io
import cv2
from api.tasks.worker import add_avi, add
import base64

router = APIRouter(
    prefix='/face-recognition',
    tags=['Face recognition'],
    responses={404: {'description': 'Not Found'}}
)


@router.post('/train')
async def train(username: str, file: UploadFile, task: BackgroundTasks):
    video_bytes = await file.read()
    # task.add_task(aviFaceController.add_avi,video_bytes,username)
    add_avi.delay(video_bytes.hex(), username)
    # add.delay(1,2)
    return {"test": "OK"}

@router.post('/test')
async def train():
    # task.add_task(aviFaceController.add_avi,video_bytes,username)
    # add_avi.delay(video_bytes.hex(), username)
    add.delay(1,2)
    return {"test": "OK"}

@router.post('/recognition')
async def recognition(file: bytes = File()):
    img = Image.open(io.BytesIO(file))
    image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    result = await aviFaceController.recognition(image)
    return {'result': result}
