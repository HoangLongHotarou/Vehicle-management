import base64
import io
import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, File, APIRouter
from fastapi.responses import FileResponse, Response, StreamingResponse
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from ONNXModel.processing import processing
# from yolo_function.yoloV7.processing import YOLOV7Processing
# from yolo_function.yoloV5.processing import YOLOV5Processing

import time

# test = YOLOV5Processing()
# test = YOLOV7Processing()

app = FastAPI(
    openapi_url='/api/v1/yolo-license-plate/openapi.json',
    docs_url='/api/v1/yolo-license-plate/docs',
    redoc_url='/api/v1/yolo-license-plate/redoc',
    title='YOLO detect license plate',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)

router = APIRouter(prefix='/api/v1/yolo-license-plate',responses={'404':{'description':'Not found test'}})

@router.post('/images/detect')
async def detect_image(file:bytes = File()):
    img = Image.open(io.BytesIO(file))
    image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    start = time.time()
    labels = processing(image)
    # labels = test.predict(image)
    end = time.time()
    return {"list":labels,"time":end-start}


# @router.post('/images/detect')
# async def detect_image(file:bytes = File()):
#     img = Image.open(io.BytesIO(file))
#     image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     start = time.time()
#     labels = processing(image)
#     end = time.time()
#     return {"list":labels,"time":end-start}


@router.post('/images/predict')
async def detect_image(file:bytes = File()):
    image_base64 = np.fromstring(base64.b64decode(file), dtype=np.uint8)
    image_base64 = cv2.imdecode(image_base64, cv2.IMREAD_ANYCOLOR)
    # labels = processing(image_base64)
    labels = processing(image)
    # labels = test.predict(image)
    return labels

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level='info'
    )
