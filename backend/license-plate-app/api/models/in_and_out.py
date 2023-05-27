from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from base.models import BaseModel
from base.schema import IDSchema, PaginationInfo
from pydantic import EmailStr, Field
from utils.pyobjectid import ObjectId, PyObjectId
from .in_and_out_time import InAndOutTimeModelOut
from .region import RegionModelOut, SearchRegionModel
from .vehicle import VehicleModelOut, SearchVehicle

class InAndOutModel(BaseModel):
    id_vehicle: PyObjectId = Field(...)
    id_region: PyObjectId = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id_vehicle": "PyObjectId",
                "id_region": "PyObjectId",
            }
        }

class InAndOutModelOut(InAndOutModel,IDSchema):
    pass

class InAndOutModelV2(BaseModel):
    vehicle: Optional[VehicleModelOut]
    region: Optional[RegionModelOut]
    in_and_out_time: Optional[InAndOutTimeModelOut]

class InAndOutModelOutV2(InAndOutModelV2,IDSchema):
    pass

class SelectType(str,Enum):
    turn_in = 'in'
    turn_out = 'out'

class InAndOutModelListOut(PaginationInfo):
    list: Optional[List[InAndOutModelOut]]


class InAndOutModelListOutV2(BaseModel):
    total: Optional[int]=0
    pages_size: Optional[int]=0
    page: Optional[int]=0
    limit: Optional[int]=0
    total_in_and_out: Optional[int]=0
    total_in: Optional[int]=0
    total_out: Optional[int]=0
    list: Optional[List[InAndOutModelOutV2]]


class Time(BaseModel):
    start_time: Optional[str]
    end_time: Optional[str]

class Date(BaseModel):
    start_date: Optional[str]
    end_date: Optional[str]
    
class Search(BaseModel):
    date: Optional[Date]
    time_in: Optional[Time]
    time_out: Optional[Time]
    region: Optional[SearchRegionModel]
    vehicle: Optional[SearchVehicle]

class GetInOutForUser(BaseModel):
    date: Optional[Date]
    region_id: Optional[PyObjectId]
    plate: Optional[str]