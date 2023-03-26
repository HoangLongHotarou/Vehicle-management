from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks, File, status
from fastapi.responses import JSONResponse
from api.controllers.controller import faceRecognitionController
import numpy as np
from core.config import settings
from PIL import Image
import io
import cv2
from api.tasks.worker import task_train, add
import base64

router = APIRouter(
    prefix='/face-recognition',
    tags=['Face recognition'],
    responses={404: {'description': 'Not Found'}}
)


@router.post('/train')
async def train(username: str, file: UploadFile):
    info = await faceRecognitionController.get_face(username)
    if info == None:
        video_bytes = await file.read()
        task_train.delay(video_bytes.hex(), username)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                'detail':f'{username} đang được xử lý'
            }
        )
    return JSONResponse(
        status_code=status.HTTP_302_FOUND,
        content={
            'detail':f'{username} đã tồn tại trong dữ liệu nhận dạng khuôn mặt'
        }
    )

# @router.post('/test')
# async def train():
#     add.delay(1,2)
#     return {"test": "OK"}

@router.post('/recognition')
async def recognition(file: bytes = File()):
    img = Image.open(io.BytesIO(file))
    image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    result = await faceRecognitionController.recognition(image)
    return {'list': result}


@router.post('/test')
async def test():
    await faceRecognitionController.reload_model()
    return "test"
