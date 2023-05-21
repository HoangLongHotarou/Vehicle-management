import json

import aiohttp
import requests
from fastapi import status
from fastapi.exceptions import HTTPException
from utils.singleton import SingletonMeta

class FetchAuthAPI(metaclass=SingletonMeta):
    def __init__(self):
        self.url = 'http://auth_service:8000/api/v1/auth'
        # self.url = 'http://localhost:8001/api/v1/auth'
        self.key = 'c20c4a219481f901'

    async def get_user_by_username(self,username):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.url}/user/get_user_by_username/{username}?key={self.key}') as response:
                if response.status==200:
                    return await response.json()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='network bad request')

    async def get_user(self,id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.url}/user/get_user/{id}?key={self.key}') as response:
                if response.status==200:
                    return await response.json()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='network bad request')

    async def get_user_list(self,ids):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.url}/user/get_user_list/?key={self.key}',json=ids) as response:
                if response.status==200:
                    return await response.json()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='network bad request')

    async def get_permission_follow_user(self, id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.url}/user/get_user_permission/{id}?key={self.key}') as response:
                if response.status==200:
                    return await response.json()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='network bad request')

    async def login(self,user):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.url}/user/login',json=user) as response:
                if response.status==200:
                    return await response.json()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='email or password incorrect')