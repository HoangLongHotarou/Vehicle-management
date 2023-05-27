from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from base.models import BaseModel
from pydantic import EmailStr, Field
from utils.pyobjectid import ObjectId, PyObjectId
from api.models.vehicle import VehicleType
from api.models.in_and_out_time import Type

class CoordinateSchema(BaseModel):
    x0: Optional[str]
    y0: Optional[str]
    x1: Optional[str]
    y1: Optional[str]

class PlateSchema(BaseModel):
    plate: Optional[str]
    coordinate: Optional[CoordinateSchema]

class CheckInAndOutSchema(BaseModel):
    plates: Optional[List[PlateSchema]]
    id_region: Optional[PyObjectId]
    turn: Optional[Type]
    image_base64: Optional[str]

# class CheckInAndOutSchema(BaseModel):
#     plate: Optional[str]
#     id_region: Optional[PyObjectId]
#     turn: Optional[Type]