from functools import wraps

from api.services.fetchapi import FetchAuthAPI
from fastapi import status
from fastapi.exceptions import HTTPException

fetchAuthAPI = FetchAuthAPI()

def check_has_permission(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        current_user = kwargs['current_user']
        user = await fetchAuthAPI.get_permission_follow_user(current_user['id'])
        for role in user['roles']:
            if func.__name__ in role['permissions']:
                return await func(*args,**kwargs)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail='user is not staff member')
    return wrapper