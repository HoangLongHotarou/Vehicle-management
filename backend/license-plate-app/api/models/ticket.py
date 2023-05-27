from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from base.models import BaseModel
from base.schema import IDSchema, PaginationInfo
from pydantic import EmailStr, Field
from typing import List
from utils.pyobjectid import ObjectId, PyObjectId
from .in_and_out_time import InAndOutTimeModelOut
from .region import RegionModelOut, SearchRegionModel
from .vehicle import VehicleModelOut, SearchVehicle, VehicleType

class TicketType(str,Enum):
    month="month"
    year="motorcycle"

class RegisterDate(BaseModel):
    register_type: TicketType
    created_at: str
    expire_at: str
    price: str

class TicketModel(BaseModel):
    user_id:  PyObjectId
    vehicle_type: VehicleType
    register_date: List[RegisterDate]


class TicketUserSchema(BaseModel):
    vehicle_type: VehicleType
    ticket_type: TicketType