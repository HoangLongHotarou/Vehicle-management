from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class SendOTP(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    phone_number: Optional[str]
    password: Optional[str]
    otp: Optional[str]
    created_at: Optional[datetime]


class ConfirmOTP(BaseModel):
    email: EmailStr = Field(...)
    otp: str = Field(...)