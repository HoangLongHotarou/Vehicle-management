from core.jwt import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from api.controllers.auth import AuthController


router = APIRouter(
    prefix='/auth',tags=['Auth'],responses={404: {'description': 'Not found'}}
)

@router.post('/oauth2/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    authCtrl = AuthController()
    username = form_data.username
    password = form_data.password
    user_lg = {'username':username,'password':password}
    token = await authCtrl.login(user_lg)
    return token
