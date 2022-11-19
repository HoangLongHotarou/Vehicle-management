import asyncio
import base64
import concurrent.futures
import threading
import time

import cv2
# from api.controllers.region import RegionController
from fastapi import status
from utils.pyobjectid import PyObjectId

# from multiprocessing import Process
from services.fetchapi import FetchVehicleManager, FetchYoloAPI

try:
    from greenlet import getcurrent as get_ident
except:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident

class CameraEvent(object):
    def __init__(self):
        self.events = {}

    def wait(self):
        ident = get_ident()
        if ident not in self.events:
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        now = time.time()
        remove = []
        for ident, event in self.events.items():
            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 5:
                    remove.append(ident)
        for ident in remove:
            del self.events[ident]

    def clear(self):
        self.events[get_ident()][0].clear()


class BaseCamera:
    thread = None 
    frame = None 
    last_access = 0
    event = CameraEvent()

    def __init__(self):
        if self.thread is None:
            self.last_access = time.time()
            self.thread = threading.Thread(target=self._thread)
            self.thread.start()
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        self.last_access = time.time()
        self.event.wait()
        self.event.clear()
        return self.frame

    def frames(self)->any:
        raise RuntimeError('Must be implemented by subclasses.')

    def _thread(self):
        print('[INFO] Starting camera thread.')
        frames_iterator = self.frames()
        for frame in frames_iterator:
            self.frame = frame
            self.event.set()
            time.sleep(0)
            if time.time() - self.last_access > 10:
                frames_iterator.close()
                print('[INFO] Stopping camera thread due to inactivity.')
                break
        self.thread = None


class CameraStream(BaseCamera):
    def __init__(self,id_region,turn,src=0,manager=None,task=None):
        self.src = src
        self.id_region = id_region
        self.turn = turn
        self.manager=manager
        self.fetchYoloAPI = FetchYoloAPI()
        self.fetchVehicleManager = FetchVehicleManager()
        self.task = task
        
        super().__init__()

    def useAI(self,img):
        _, im_arr = cv2.imencode('.jpg', img)
        im_bytes = im_arr.tobytes()
        image = base64.b64encode(im_bytes)
        
        plates = asyncio.run(self.fetchYoloAPI.predict(image))
        
        if plates == [] or plates == None:
            return
        
        object = {
            'plates': plates,
            'id_region': str(self.id_region),
            'turn': self.turn,
            'vehicle_type': 'motorcycle'
        }
        # data =object
        data = asyncio.run(
            self.fetchVehicleManager.check_turn_in_out(object)
        )
        print(data)
        if data != []:
            asyncio.run(self.manager.broadcast(data,self.id_region))

    def frames(self)->any:
        frame = cv2.VideoCapture(self.src)
        count = 0
        try:
            while True:
                success, img = frame.read()
                if not success:
                    print('cannot connect camera')
                    break
                count += 1
                if count%50==0: 
                    count=0
                    thread = threading.Thread(target=self.useAI,args=(img,))
                    thread.start()
                yield cv2.imencode('.jpg', img)[1].tobytes()
        except Exception as e:
            print(e)
