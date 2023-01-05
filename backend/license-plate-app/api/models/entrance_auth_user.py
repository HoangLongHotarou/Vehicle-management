from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from base.models import BaseModel
from base.schema import IDSchema, PaginationInfo
from pydantic import EmailStr, Field,AnyUrl
from utils.pyobjectid import ObjectId, PyObjectId
from api.models.entrance_auth import EntranceAuthModel

class User(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    avatar: Optional[AnyUrl]

class EntranceAuthUserModel(BaseModel):
    id_user: PyObjectId = Field(...)
    id_entrance_auth: PyObjectId = Field(...)
    enable: bool = True

class EntranceAuthStudentModel(BaseModel):
    id_user: PyObjectId = Field(...)
    enable: bool = True

class EntranceAuthUserModelOut(EntranceAuthUserModel, IDSchema):
    pass

class EntranceAuthUserListModelOut(PaginationInfo):
    list: Optional[List[EntranceAuthUserModelOut]]

class EntranceAuthUserModelV2(BaseModel):
    user: Optional[User]
    entrance_auth: Optional[EntranceAuthModel]

class EntranceAuthUserModelV2Out(EntranceAuthUserModelV2,IDSchema):
    pass

class EntranceAuthUserListModelV2Out(PaginationInfo):
    list: Optional[List[EntranceAuthUserModelV2Out]]