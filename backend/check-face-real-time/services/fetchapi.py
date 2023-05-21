import json

import aiohttp
import requests
from fastapi import status
from fastapi.exceptions import HTTPException
from utils.singleton import SingletonMeta


class FetchFaceRecognitionAPI(metaclass=SingletonMeta):
    def __init__(self):
        self.url = 'http://0.0.0.0:8005/api/v1/vehicle-face-recognition'
        # self.url = 'http://127.0.0.1:8002/api/v1/yolo-license-plate'
    
    async def predict(self,image):
        data = aiohttp.FormData()
        data.add_field("file", image)
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.url}/face-recognition/recognition/one-user',data=data) as response:
                if response.status==200:
                    return await response.json()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='network bad request')

class FetchVehicleManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        # self.url = 'http://app_service:8000/api/v1/license-plate-app'
        self.url = 'http://127.0.0.1:8003/api/v1/license-plate-app'
    
    async def check_turn_in_out(self,data):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.url}/in_and_out/check_turn_in_out_realtime',json=data) as response:
                if response.status==200:
                    return await response.json()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='network bad request')

    async def get_region(self,id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.url}/regions/{id}') as response:
                if response.status==200:
                    return await response.json()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='network bad request')