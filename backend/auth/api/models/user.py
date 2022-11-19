from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

import pydantic
from base.models import BaseModel
from base.schema import IDSchema, PaginationInfo
from pydantic import AnyUrl, EmailStr, Field
from utils.pyobjectid import ObjectId, PyObjectId

regex_phone_number = pydantic.constr(regex="[0-9]{9,10}")
# regex_password = pydantic.constr(regex=".{8,}")

class UserModel(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)
    phone_number: regex_phone_number = Field(...)
    password: str = Field(...)
    first_name: str = None
    last_name: str = None
    avatar: AnyUrl = None
    roles: List[PyObjectId] = []
    is_staff: bool = False

    class Config:
        schema_extra = {
            "example": {
                "email": "str@gmail.com",
                "username": "str",
                "phone_number":"0911445111",
                "password": "str"
            }
        }

class AccountUserModel(BaseModel):
    username: Optional[str]

class UpdateUserModel(BaseModel):
    phone_number: Optional[regex_phone_number]
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "phone_number": "phone-number",
                "first_name": "str",
                "last_name": "str",
            }
        }

class UpdateAvatar(BaseModel):
    avatar: Optional[AnyUrl]

class SendEmail(BaseModel):
    email: EmailStr = Field(...)

class UserModelOut(UpdateAvatar,UpdateUserModel,AccountUserModel,SendEmail,IDSchema):
    pass

class UserModelListOut(PaginationInfo):
    list: List[UserModelOut]

class Current_User(IDSchema):
    username: Optional[str]

class UserLogin(BaseModel):
    username: Optional[str]
    password: Optional[str]

class UpdateRolesUser(BaseModel):
    roles: Optional[List[PyObjectId]]

class ResetPassword(BaseModel):
    token: str
    password: str