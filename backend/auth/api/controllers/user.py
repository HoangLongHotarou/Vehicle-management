from datetime import datetime

import cloudinary.uploader
from api.models.otp import SendOTP
from api.models.user import UpdateAvatar, UserModel, UserModelOut
from api.services.crud import OTPCrud, RoleCrud, UserCrud
from core.config import settings
from core.jwt import (create_access_token, get_current_user, get_password_hash,
                      verify_password)
from core.send_email import create_otp_confirm, send_otp
from fastapi import status
from fastapi.exceptions import HTTPException
from pymongo import IndexModel
from utils.pyobjectid import PyObjectId
from utils.singleton import SingletonMeta
from db.database import get_database

import asyncio

db = asyncio.run(get_database())

class UserController(metaclass=SingletonMeta):
    def __init__(self, ):
        self.db = db
        self.roleCrud = RoleCrud()
        self.userCrud = UserCrud()
        self.otpCrud = OTPCrud()

    async def update_avatar(self,id,file):
        user = await self.userCrud.get(value=id,projection={'avatar':1})
        url = user.get('avatar')
        if url != None:
            public_id = url.rsplit('/',1)[1].split('.')[0]
            cloudinary.uploader.destroy(f'{settings.STORE}/{public_id}')
        result = cloudinary.uploader.upload(file,folder=settings.STORE)
        url = result.get('url')
        update_avatar = UpdateAvatar(avatar=url)
        await self.userCrud.update(value=id, config_data=update_avatar.dict())
        return url


    async def register(self, user: UserModel, task):
        await self.userCrud.set_multi_unique()
        checks = {}
        check_username = await self.userCrud.get(query={'username': user.username})
        check_email = await self.userCrud.get(query={'email': user.email})
        check_phone_number = await self.userCrud.get(query={'phone_number': user.phone_number})
        checks[user.username] = check_username
        checks[user.email] = check_email
        checks[user.phone_number] = check_phone_number
        announce = ""
        for key in checks:
            if checks[key] is not None:
                announce += f'{key} '
        if announce != "":
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail=f'{announce}đã tồn tại')
        user.password = get_password_hash(user.password)
        otp = create_otp_confirm()
        sendOTP = SendOTP(**{**user.dict(),**{'otp':otp,'created_at':datetime.utcnow()}})
        await self.otpCrud.add(sendOTP.dict())
        task.add_task(
            send_otp, "Xác nhận đăng kí tài khoản",user.email,{
                'title': "Xác nhận đăng kí tài khoản",
                'name': user.email,
                'OTP': otp
            }
        )

    async def confirm_register(self, confirmOTP):
        OTPs = []
        OTPs,_ = await self.otpCrud.get_all(query={'email':confirmOTP.email})
        if OTPs == []:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Địa chỉ email không hợp lệ')
        otp_user = OTPs[len(OTPs)-1]
        if otp_user['otp']==confirmOTP.otp:
            user = UserModel(**otp_user)
            await self.userCrud.add(user.dict())
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='OTP không hợp lệ')

    async def forget_password(self,user,task):
        check_email = await self.userCrud.get(query={'email': user.email})
        if check_email is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail=f'{user.email} chưa được đăng ký')
        otp = create_otp_confirm()
        sendOTP = SendOTP(**{**user.dict(),**{'otp':otp,'created_at':datetime.utcnow()}})
        await self.otpCrud.add(sendOTP.dict())
        task.add_task(
            send_otp, "Xác nhận reset mật khẩu",user.email,{
                'title': "Xác nhận reset mật khẩu",
                'name': user.email,
                'OTP': otp
            }
        )
    
    async def confirm_forget_password(self,confirmOTP):
        OTPs = []
        OTPs,_ = await self.otpCrud.get_all(query={'email':confirmOTP.email})
        if OTPs == []:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Địa chỉ email không hợp lệ')
        otp_user = OTPs[len(OTPs)-1]
        if otp_user['otp']==confirmOTP.otp:
            user = await self.userCrud.get(query={'email':confirmOTP.email})
            token = create_access_token(user)
            return token
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='OTP không hợp lệ')

    async def reset_password(self,resetPassword):
        token_user = get_current_user(resetPassword.token)
        await self.userCrud.update(
            value=token_user.id, 
            config_data={'password':get_password_hash(resetPassword.password)}
        )

    async def login(self, user_lg: UserModel):
        user = await self.userCrud.get(query={'username': user_lg.username})
        if user is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail=f'incorrect username or password')
        is_valid = verify_password(user_lg.password, user['password'])
        if is_valid == False:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail=f'incorrect username or password')
        return {
            'user': UserModelOut(**user),
            'access_token': create_access_token(user),
            'token_type': "bearer"
        }

    async def delete_user(self,id_user):
        async with await self.db.mongodb_client.start_session() as session:
            async with session.start_transaction():
                await self.userCrud.delete(value=id_user,session=session)
                roles,_ = await self.roleCrud.get_all(query={'users':PyObjectId(id_user)},projection={'_id':1})
                if roles != []:
                    ids_roles = [role['_id'] for role in roles]
                    await self.roleCrud.pull_user(ids_roles, id_user, session)

    async def get_permission(self,id_user):
        user = await self.userCrud.get(value=id_user,projection={'roles':1,'is_staff':1})
        roles,_ = await self.roleCrud.get_all(query={'_id':{'$in':user['roles']}},projection={'_id':0,'role':1,'permissions':1})
        return {'is_staff':user.get('is_staff',False),'roles':roles}

    async def update_roles(self,id_user,data):
        async with await self.db.mongodb_client.start_session() as session:
            async with session.start_transaction():
                await self.userCrud.update(value=id_role, config_data=data.dict(),session=session)
                roles,_ = await self.roleCrud.get_all(query={'$or':[{'_id':{'$in':data.roles}},{'users':PyObjectId(id_user)}]})
                push_user_roles = []
                pull_user_roles = []
                for role in roles:
                    id_role = PyObjectId(role['_id'])
                    if id_role not in data.roles and PyObjectId(id_role) in role['users']:
                        pull_user_roles.append(id_role)
                    if id_role in data.users and PyObjectId(id_role) not in role['users']:
                        push_user_roles.append(id_role)
                if pull_user_roles != []:
                    await self.roleCrud.pull_user(ids_role=pull_user_roles, id_user=id_user,session=session)
                if push_user_roles != []:
                    await self.roleCrud.push_user(ids_role=push_user_roles, id_user=id_user,session=session)
