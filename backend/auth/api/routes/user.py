from typing import List

from api.controllers.user import UserController
from api.models.otp import ConfirmOTP
from api.models.user import (ResetPassword, SendEmail, UpdateRolesUser,
                             UpdateUserModel, UserLogin, UserModel,
                             UserModelListOut, UserModelOut)
from core.config import settings
from core.jwt import OAuth2PasswordRequestForm, get_current_user
from fastapi import (APIRouter, BackgroundTasks, Depends, File, Query,
                     UploadFile, status)
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from utils.decorators import check_is_staff, check_is_staff_or_permission
from utils.pagination import pagination_info
from utils.pyobjectid import PyObjectId
import re

router = APIRouter(
    prefix='/user',
    tags=['User'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/register')
async def register_user(user: UserModel, task: BackgroundTasks):
    userCtrl = UserController()
    await userCtrl.register(user, task)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            'detail': 'Email đã được gửi với otp để xác nhận tạo tài khoản'
        }
    )

@router.post('/create-account')
@check_is_staff_or_permission
async def create_account_by_admin(
    user: UserModel,
    current_user=Depends(get_current_user)
):
    userCtrl = UserController()
    await userCtrl.create_account(user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'detail': 'Tài khoản tạo thành công'
        }
    )


@router.post('/confirm_register')
async def confirm_register(confirmOTP: ConfirmOTP):
    userCtrl = UserController()
    await userCtrl.confirm_register(confirmOTP)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'detail': 'Đã tạo tài khoản thành công'
        }
    )


@router.post('/oauth2/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    userCtrl = UserController()
    user_lg = UserLogin(username=username, password=password)
    token = await userCtrl.login(user_lg)
    return token


@router.post('/login')
async def login(user_lg: UserLogin):
    userCtrl = UserController()
    token = await userCtrl.login(user_lg)
    return token


@router.post('/forget_password')
async def forget_password(user: SendEmail, task: BackgroundTasks):
    userCtrl = UserController()
    await userCtrl.forget_password(user, task)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            'detail': 'OTP đã được gửi tới Email của bạn để reset lại mật khẩu'
        }
    )


@router.post('/confirm_forget_password')
async def confirm_forget_password(confirmOTP: ConfirmOTP):
    userCtrl = UserController()
    token = await userCtrl.confirm_forget_password(confirmOTP)
    return {'reset_token': token}


@router.post('/reset_password')
async def reset_password(resetPassword: ResetPassword):
    userCtrl = UserController()
    await userCtrl.reset_password(resetPassword)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            'detail': 'reset mật khẩu thành công'
        }
    )


@router.get('/users')
@check_is_staff_or_permission
async def get_all_user(
        page: int = Query(0, ge=0),
    limit: int = Query(20, ge=0, le=20),
    search: str = None,
    current_user=Depends(get_current_user)
):
    userCtrl = UserController()
    if search:
        query={
            'username': re.compile(f'{search}', re.IGNORECASE)
        }
    else:
        query = {}
    users, info = await userCtrl.userCrud.get_all(
        query,
        is_get_info=True,
        page=page,
        limit=limit
    )
    dict = pagination_info(users, info)
    return UserModelListOut(**dict)


@router.get('/users/me', response_model=UserModelOut)
async def get_me(current_user=Depends(get_current_user)):
    userCtrl = UserController()
    user = await userCtrl.userCrud.get(value=current_user.id)
    return user


@router.put('/users/me')
async def update_me(update_user: UpdateUserModel, current_user=Depends(get_current_user)):
    userCtrl = UserController()
    await userCtrl.userCrud.update(value=current_user.id, config_data=update_user.dict())
    return {'detail': 'update successfully'}


@router.put('/users/me/avatar')
async def get_my_avatar(
    file: UploadFile,
    current_user=Depends(get_current_user)
):
    max_size = 500
    # if file.content_type != 'image/jpeg' and file.content_type != 'image/png':
    #     raise HTTPException(
    #         status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='không phải hình ảnh')
    content = await file.read()
    file_size = len(content)
    if file_size > max_size*1024:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
            detail=f'dung lượng hình ảnh không được quá {max_size} KB'
        )
    userCtrl = UserController()
    url = await userCtrl.update_avatar(id=current_user.id, file=content)
    return {'avatar': url}


@router.get('/users/{id_user}', response_model=UserModelOut)
@check_is_staff_or_permission
async def get_user(id_user: str, current_user=Depends(get_current_user)):
    userCtrl = UserController()
    user = await userCtrl.userCrud.get(value=id_user)
    return user


@router.get('/get_user/{id_user}', response_model=UserModelOut)
async def system_get_user(id_user: str, key: str):
    userCtrl = UserController()
    if key != settings.PATH_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='key not allow')
    user = await userCtrl.userCrud.get(value=id_user)
    return user

@router.post('/get_user_list', response_model=List[UserModelOut])
async def system_get_user_list(ids_user: List[PyObjectId], key: str):
    userCtrl = UserController()
    #c20c4a219481f901
    if key != settings.PATH_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='key not allow')
    users,_ = await userCtrl.userCrud.get_all(query={'_id':{'$in':ids_user}})
    return users

@router.get('/get_user_permission/{id_user}')
async def get_user_permission(id_user: str, key: str):
    userCtrl = UserController()
    if key != settings.PATH_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='key not allow')
    roles = await userCtrl.get_permission(id_user)
    return roles


@router.get('/get_user/{id_user}', response_model=UserModelOut)
async def system_get_permission(id_user: str, key: str):
    userCtrl = UserController()
    if key != settings.PATH_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='key not allow')
    user = await userCtrl.userCrud.get(value=id_user)
    return user


@router.put('/users/{id_user}')
@check_is_staff_or_permission
async def update_user(
    id_user: str, 
    update_user: UpdateUserModel, 
    current_user=Depends(get_current_user)
):
    userCtrl = UserController()
    await userCtrl.userCrud.update(value=id_user, config_data=update_user.dict())
    return {'detail': 'update successfully'}


@router.delete('/users/{id_user}')
@check_is_staff_or_permission
async def delete_user(id_user: str, current_user=Depends(get_current_user)):
    userCtrl = UserController()
    await userCtrl.delete_user(id_user=id_user)
    return {'detail': 'delete successfully'}


@router.put('/users/{id_user}/update_roles')
@check_is_staff_or_permission
async def update_role_user(id_user: str, data: UpdateRolesUser):
    userCtrl = UserController()
    await userCtrl.update_roles(id_user, data)
    return {'detail': 'Update successfully'}


# @router.post('/upload_image')
# async def test_add_image(file: UploadFile):
#     result = cloudinary.uploader.upload(file.file, folder='my_images/users')
#     url = result.get('url')
#     # print(result.get('public_id'))
#     print(url.rsplit('/', 1)[1].split('.')[0])
#     return url


# @router.delete('upload_image/{public_id}')
# async def test_delete_image(public_id: str):
#     a = cloudinary.uploader.destroy(public_id, folder='my_images/users')
#     print(a)
#     return {"test": "test"}
