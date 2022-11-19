from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from base.models import BaseModel
from pydantic import EmailStr, Field
from utils.pyobjectid import ObjectId, PyObjectId


class BookAppointmentModel(BaseModel):
    region_id: PyObjectId = Field(...)
    user_id: PyObjectId = Field(...)
    book_date: datetime = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "region_id": "PyObjectId",
                "user_id": "PyObjectId",
                "book_date": "datetime"
            }
        }