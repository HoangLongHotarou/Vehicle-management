import json

import aiohttp
import requests
from fastapi import status
from fastapi.exceptions import HTTPException
from utils.singleton import SingletonMeta

class FetchVehicleManagement(metaclass=SingletonMeta):
    def __init__(self):
        self.url = 'http://app_service:8000/api/v1/license-plate-app'
        # self.url = 'http://127.0.0.1:8002/api/v1/yolo-license-plate'
    
    async def set_student_role(self,data):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.url}/entrance_auth/users/student',json=data) as response:
                if response.status==200:
                    return await response.json()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='network bad request')