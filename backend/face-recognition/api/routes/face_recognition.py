from fastapi import APIRouter, Depends, Query, UploadFile, BackgroundTasks, File, status
from fastapi.responses import JSONResponse
from typing import Union
from api.controllers.controller import faceRecognitionCtrl
from core.config import settings
from api.tasks.worker import task_train, add
from api.models.face_recognition_info import FaceRecognitionInfoListOut
from api.models.options import TrainOptions
from PIL import Image
from utils.pagination import pagination_info
import numpy as np
import io
import cv2
import base64
import time

router = APIRouter(
    prefix='/face-recognition',
    tags=['Face recognition'],
    responses={404: {'description': 'Not Found'}}
)


@router.get('/get-info', response_model=FaceRecognitionInfoListOut)
async def get_info(
    page: int = Query(0, ge=0),
    limit: int = Query(20, ge=0, le=20)
):
    faceRecognitionInfos, info = await faceRecognitionCtrl.infoCrud.get_all(
        is_get_info=True,
        page=page,
        limit=limit
    )
    dict = pagination_info(faceRecognitionInfos, info)
    return dict


@router.post('/train')
async def train(
    username: str,
    file: UploadFile,
    train_option: Union[TrainOptions, None] = None
):
    info = await faceRecognitionCtrl.get_face(username)
    option = None if train_option == None else train_option.value
    if info == None or option != None:
        if info:
            info['_id'] = str(info['_id'])
        video_bytes = await file.read()
        
        print(video_bytes)
        
        task_train.delay(
            video_bytes.hex(), 
            username, 
            option, 
            info
        )
        
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                'detail': f'{username} đang được xử lý'
            }
        )
    elif info.get('len_embs') != 0:
        return JSONResponse(
            status_code=status.HTTP_302_FOUND,
            content={
                'detail': f'{username} đã tồn tại trong dữ liệu nhận dạng khuôn mặt'
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_302_FOUND,
            content={
                'detail': f'{username} đang train nếu 20 phút sau chưa có thì vui lòng train lại'
            }
        )


@router.post('/recognition/one-user')
async def recognition_one_user(file: bytes = File()):
    start = time.time()
    image_base64 = np.fromstring(base64.b64decode(file), dtype=np.uint8)
    image_base64 = cv2.imdecode(image_base64, cv2.IMREAD_ANYCOLOR)
    result = await faceRecognitionCtrl.recognition_one_user(image_base64)
    end = time.time()
    return {'list': result, 'time': float(end-start)}

@router.post('/recognition/one-user/test')
async def recognition_one_user(file: bytes = File()):
    start = time.time()
    img = Image.open(io.BytesIO(file))
    image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    result = await faceRecognitionCtrl.recognition_one_user(image)
    end = time.time()
    return {'list': result, 'time': float(end-start)}

@router.post('/recognition')
async def recognition(file: bytes = File()):
    start = time.time()
    image_base64 = np.fromstring(base64.b64decode(file), dtype=np.uint8)
    image_base64 = cv2.imdecode(image_base64, cv2.IMREAD_ANYCOLOR)
    result = await faceRecognitionCtrl.recognition(image_base64)
    end = time.time()
    return {'list': result, 'time': float(end-start)}

@router.post('/recognition/test')
async def recognition(file: bytes = File()):
    start = time.time()
    img = Image.open(io.BytesIO(file))
    image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    result = await faceRecognitionCtrl.recognition(image)
    end = time.time()
    return {'list': result, 'time': float(end-start)}

@router.delete('/remove-face/{username}')
async def remove_face(username: str):
    await faceRecognitionCtrl.remove_face(username)
    return {"test": "finish"}
