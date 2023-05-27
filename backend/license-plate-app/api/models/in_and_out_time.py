from enum import Enum
from typing import List, Optional, Union

from base.models import BaseModel
from base.schema import IDSchema, PaginationInfo
from pydantic import EmailStr, Field
from utils.pyobjectid import PyObjectId


class Type(str,Enum):
    turn_in = 'in'
    turn_out = 'out'

class Time(BaseModel):
    time: Optional[str]
    type: Optional[Type]
    vehicle_img_base64: Optional[str]
    face_img_base64: Optional[str]

class InAndOutTimeModel(BaseModel):
    id_in_and_out: Optional[PyObjectId]
    date: Optional[str]
    times: Optional[List[Time]]=[]

class InAndOutTimeModelOut(InAndOutTimeModel,IDSchema):
    pass

class InAndOutTimeModelListOut(PaginationInfo):
    list: Optional[List[InAndOutTimeModelOut]]