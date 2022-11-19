import time

from utils.pyobjectid import PyObjectId
from utils.websocket import ConnectionManagerV2
from utils.stream import CameraStream
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

stream = {}
def video_streaming_generator(camera_streaming):
    while True:
        frame = camera_streaming.get_frame()
        time.sleep(0.25)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get('/api/v1/check-vehicle-real-time/camera')
def video_feed(id_region: str,type: str,rtsp: str):
    url = rtsp
    if url not in stream.keys() or stream[url].thread==None:
        stream[url] = CameraStream(id_region,type,url,test_manager)
    return StreamingResponse(
        video_streaming_generator(stream[url]),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )

@app.get('/api/v1/check-vehicle-real-time/get_rtsp_from_region/{id_region}')
async def get_rtsp_from_region(request: Request,id_region: PyObjectId):
    region = await vehicleCtrl.get_region(id_region)
    cameras = region.get('cameras')
    if cameras == None: cameras=[]
    for i in range(len(cameras)):
        urls= request.url_for(
            'video_feed',
        )
        urls = urls+f"?id_region={id_region}&type={cameras[i]['type']}&rtsp={cameras[i]['rtsp_url']}"
        cameras[i]['rtsp_url']=urls
    return cameras


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level='info'
    )
