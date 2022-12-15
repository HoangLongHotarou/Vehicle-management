from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from base.models import BaseModel
from base.schema import IDSchema, PaginationInfo
from pydantic import EmailStr, Field,AnyUrl
from utils.pyobjectid import ObjectId, PyObjectId
from api.models.region import RegionModelOutForEntrance
from api.models.entrance_auth import EntranceAuthModel



class EntranceAuthRegionModel(BaseModel):
    id_region: PyObjectId = Field(...)
    id_entrance_auth: PyObjectId = Field(...)
    enable: bool = True

class EntranceAuthRegionModelOut(EntranceAuthRegionModel, IDSchema):
    pass

class EntranceAuthRegionModelV2(BaseModel):
    region: Optional[RegionModelOutForEntrance]
    entrance_auth: Optional[EntranceAuthModel]

class EntranceAuthRegionModelV2Out(EntranceAuthRegionModelV2,IDSchema):
    pass

class EntranceAuthRegionListModelOut(PaginationInfo):
    list: Optional[List[EntranceAuthRegionModelOut]]

class EntranceAuthRegionListModelV2Out(PaginationInfo):
    list: Optional[List[EntranceAuthRegionModelV2Out]]