import time

from utils.pyobjectid import PyObjectId
from utils.websocket import ConnectionManagerV2
from utils.stream import VehicleCameraStream, FaceCameraStream
from services.fetchapi import FetchVehicleManager

import uvicorn

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    openapi_url='/api/v1/check-vehicle-real-time/openapi.json',
    docs_url='/api/v1/check-vehicle-real-time/docs',
    redoc_url='/api/v1/check-vehicle-real-time/redoc',
    title='Check Vehicle Realtime',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)


vehicleCtrl = FetchVehicleManager()
test_manager = ConnectionManagerV2()


@app.websocket('/api/v1/check-vehicle-real-time/ws')
async def websocket_endpoint(websocket: WebSocket):
    await test_manager.connect(websocket)
    while True:
        try:
            data = await websocket.receive_json()
            test_manager.set_state_connection(websocket,status=data['status'])
        except:
            break
    test_manager.disconnect(websocket)

@app.websocket('/api/v1/check-vehicle-real-time/test_ws')
async def websocket_test(websocket: WebSocket):
    await test_manager.connect(websocket)
    while True:
        try:
            data = await websocket.receive_json()
            test_manager.set_state_connection(websocket,status=data['status'])
            await test_manager.send_personal_message(websocket,str(test_manager.activate_connection))
        except Exception as e:
            print(e)
            break
    test_manager.disconnect(websocket)

vehicle_stream = {}
face_stream = {}

def video_streaming_generator(camera_streaming):
    while True:
        frame = camera_streaming.get_frame()
        time.sleep(0.2)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get('/api/v1/check-vehicle-real-time/vehicle/camera')
def vehicle_video_feed(id_region: str,turn: str,rtsp: str):
    url = rtsp
    if url not in vehicle_stream.keys() or vehicle_stream[url].thread==None:
        vehicle_stream[url] = VehicleCameraStream(id_region,turn,url,test_manager)
    vehicle_stream[url].set_turn(turn)
    return StreamingResponse(
        video_streaming_generator(vehicle_stream[url]),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )

def face_video_streaming_generator(camera_streaming):
    while True:
        frame = camera_streaming.get_frame()
        time.sleep(0.2)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get('/api/v1/check-vehicle-real-time/face/camera')
def face_video_feed(id_region: str, turn: str, rtsp: str):
    url = rtsp
    if url not in face_stream.keys() or face_stream[url].thread == None:
        face_stream[url] = FaceCameraStream(id_region,turn,url)
    face_stream[url].set_turn(turn)
    return StreamingResponse(
        face_video_streaming_generator(face_stream[url]),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )

@app.get('/api/v1/check-vehicle-real-time/get_rtsp_from_region/{id_region}')
async def get_rtsp_from_region(request: Request,id_region: PyObjectId):
    region = await vehicleCtrl.get_region(id_region)
    cameras = region.get('cameras')
    if cameras == None: cameras=[]
    for i in range(len(cameras)):
        vehicle_urls= request.url_for(
            'vehicle_video_feed',
        )
        face_urls= request.url_for(
            'face_video_feed',
        )
        vehicle_urls = f"{vehicle_urls}?id_region={id_region}&turn={cameras[i]['type']}&rtsp={cameras[i]['rtsp_url']}"
        cameras[i]['rtsp_url']=vehicle_urls

        face_urls = f"{face_urls}?id_region={id_region}&turn={cameras[i]['type']}&rtsp={cameras[i]['face_rtsp_url']}"
        cameras[i]['face_rtsp_url']=face_urls
    return cameras


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level='info'
    )
