from functools import wraps

from api.controllers.user import UserController
from core.jwt import get_current_user
from fastapi import status
from fastapi.exceptions import HTTPException


def check_is_staff(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        current_user = kwargs['current_user']
        userCtrl = UserController()
        user = await userCtrl.userCrud.get(value=current_user.id)
        if user.get('is_staff',False)==False:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail='user is not staff member')
        return await func(*args,**kwargs)
    return wrapper

def check_is_staff_or_permission(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        current_user = kwargs['current_user']
        userCtrl = UserController()
        user = await userCtrl.get_permission(current_user.id)
        if user.get('is_staff',False)==False:
            for role in user['roles']:
                if func.__name__ in role['permissions']:
                    return await func(*args,**kwargs) 
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail='user is not staff member')
        return await func(*args,**kwargs)
    return wrapper

def check_has_permission(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        current_user = kwargs['current_user']
        userCtrl = UserController()
        user = await userCtrl.get_permission(current_user.id)
        for role in user['roles']:
            if func.__name__ in role['permissions']:
                return await func(*args,**kwargs) 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail='user is not staff member')
    return wrapper