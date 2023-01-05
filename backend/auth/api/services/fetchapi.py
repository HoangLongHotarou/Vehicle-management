import json

import aiohttp
import requests
from fastapi import status
from fastapi.exceptions import HTTPException
from utils.singleton import SingletonMeta


class FetchYoloAPI(metaclass=SingletonMeta):
    def __init__(self):
        # self.url = 'http://localhost:8002/api/v1/yolo-license-plate'
        self.url = 'http://ai_service:8000/api/v1/yolo-license-plate'
    
    async def predict(self,image):
        data = aiohttp.FormData()
        data.add_field("file", image)
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.url}/images/predict',data=data) as response:
                if response.status==200:
                    return await response.json()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='network bad request')
