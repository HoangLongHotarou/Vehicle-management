from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

import pydantic
from base.models import BaseModel
from base.schema import IDSchema, PaginationInfo
from pydantic import EmailStr, Field
from utils.pyobjectid import ObjectId, PyObjectId

regex_plate = pydantic.constr(regex="[0-9]{2}[A-Z]{1}(|[0-9]{1}|[A-Z]{1})-[0-9]{4,5}")

class VehicleType(str,Enum):
    car="car"
    motorcycle="motorcycle"

class VehicleModel(BaseModel):
    plate: regex_plate = Field(...)
    user_id: PyObjectId = Field(...)
    type: VehicleType = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "plate": "str",
                "user_id": "PyObjectId",
                "type":"Vehicle type (ex: car, motorcycle)"
            }
        }

class VehicleSubModel(BaseModel):
    plate: regex_plate = Field(...)
    type: VehicleType = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "plate": "str",
                "type":"Vehicle type (ex: car, motorcycle)"
            }
        }

class UpdateVehicleModel(BaseModel):
    plate: Optional[regex_plate]
    user_id: Optional[PyObjectId]
    type: Optional[VehicleType]

    class Config:
        schema_extra = {
            "example": {
                "plate": "str",
                "type":"Vehicle type (ex: car, motorcycle)"
            }
        }


class VehicleModelOut(UpdateVehicleModel,IDSchema):
    pass

class VehicleModelListOut(PaginationInfo):
    list: Optional[List[VehicleModelOut]]


class SearchVehicle(BaseModel):
    plate: Optional[regex_plate]
    user_id: Optional[PyObjectId]
    type: Optional[VehicleType]