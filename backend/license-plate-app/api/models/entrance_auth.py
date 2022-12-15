from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from base.models import BaseModel
from base.schema import IDSchema, PaginationInfo
from pydantic import EmailStr, Field,AnyUrl
from utils.pyobjectid import ObjectId, PyObjectId

class EntranceAuthModel(BaseModel):
    name: str = Field(...)
    enable: bool = True

class EntranceAuthModelOut(EntranceAuthModel,IDSchema):
    pass

class EntranceAuthListModelOut(PaginationInfo):
    list: Optional[List[EntranceAuthModelOut]]