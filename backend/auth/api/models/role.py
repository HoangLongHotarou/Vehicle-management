from typing import List, Optional

from base.models import BaseModel
from base.schema import IDSchema, PaginationInfo
from pydantic import Field
from utils.pyobjectid import PyObjectId


class RoleModel(BaseModel):
    role: str = Field(...)
    permissions: List[str] = Field(...)
    users: List[PyObjectId] = []

    class Config:
        schema_extra = {
            "example": {
                "role": "role name",
                "permissions": "List[str]",
            }
        }

class UpdateRoleModel(BaseModel):
    role: Optional[str]
    permissions: Optional[List[str]]
    users: Optional[List[PyObjectId]]

    class Config:
        schema_extra = {
            "example": {
                "role": "role name",
                "permissions": "List[str]",
                "users":"List[str]"
            }
        }
        

class RoleDetailModel(BaseModel):
    role: Optional[str]
    users: Optional[any]

class RoleModelOut(UpdateRoleModel,IDSchema):
    pass

class RoleDetailModelOut(RoleDetailModel, IDSchema):
    pass

class RoleModelListOut(PaginationInfo):
    list: List[RoleModelOut]

# class ModifyUserRole(BaseModel):
#     role: Optional[str]
#     users: Optional[List[PyObjectId]]