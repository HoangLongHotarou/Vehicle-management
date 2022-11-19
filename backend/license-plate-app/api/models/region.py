from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from base.models import BaseModel
from base.schema import IDSchema, PaginationInfo
from pydantic import EmailStr, Field,AnyUrl
from utils.pyobjectid import ObjectId, PyObjectId
from .in_and_out_time import Type


class CameraRTSPModel(BaseModel):
    name: Optional[str]
    rtsp_url: Optional[AnyUrl]
    type: Optional[Type]

class RegionType(str,Enum):
    parking = 'parking'
    campus = 'campus'

class Coordinate(BaseModel):
    longitude: Optional[str]
    latitude: Optional[str]

class RegionModel(BaseModel):
    region: str = Field(...)
    type: RegionType = Field(default_factory=RegionType,alias='type')
    coordinate: Optional[Coordinate]
    cameras: Optional[List[CameraRTSPModel]] = []
    acceptance_roles: Optional[List[PyObjectId]] = []

    class Config:
        schema_extra = {
            "example": {
                "region": "str",
                "type": "str",
                "coordinate":{
                    "longitude":"str",
                    "latitude":"str"
                },
            }
        }

class UpdateRegionModel(BaseModel):
    region: Optional[str]
    type: Optional[RegionType]
    coordinate: Optional[Coordinate]
    cameras: Optional[List[CameraRTSPModel]] = []

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "region": "str",
    #             "type": "str",
    #             "coordinate":{
    #                 "longitude":"str",
    #                 "latitude":"str"
    #             },
    #         }
    #     }

class RegionModelOut(UpdateRegionModel,IDSchema):
    pass

class RegionModelListOut(PaginationInfo):
    list: Optional[List[RegionModelOut]]

class SearchRegionModel(BaseModel):
    id_region: Optional[PyObjectId]
    type: Optional[RegionType]