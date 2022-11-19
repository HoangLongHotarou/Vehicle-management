from typing import Optional

from pydantic import Field
from utils.pyobjectid import PyObjectId

from .models import BaseModel


class IDSchema(BaseModel):
    id: PyObjectId =  Field(default_factory=PyObjectId, alias="_id")

class PaginationInfo(BaseModel):
    total: Optional[int]
    pages_size: Optional[int]
    page: Optional[int]
    limit: Optional[int]