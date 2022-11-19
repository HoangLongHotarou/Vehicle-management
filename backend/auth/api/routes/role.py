from api.models.role import (RoleModel, RoleModelListOut, RoleModelOut,
                             UpdateRoleModel)
from core.jwt import get_current_user
from fastapi import APIRouter, Depends, Query
from utils.decorators import check_is_staff, check_is_staff_or_permission
from utils.pagination import pagination_info
from api.controllers.controller import *

router = APIRouter(
    prefix='/roles',
    tags=['Role'],
    responses={404: {'description': 'Not found'}}
)

@router.get('/',response_model=RoleModelListOut)
@check_is_staff_or_permission
async def get_all_roles(
    page:int=Query(0,ge=0),
    limit:int=Query(20,ge=0,le=20),
    current_user=Depends(get_current_user)
):
    roles,info = await roleCtrl.roleCrud.get_all(is_get_info=True,page=page,limit=limit)
    dict = pagination_info(roles, info)
    return dict

@router.get('/{id_role}',response_model=RoleModelOut)
@check_is_staff_or_permission
async def get_role(
    id_role: str,
    current_user=Depends(get_current_user)
):
    role = await roleCtrl.roleCrud.get(value=id_role)
    return role

@router.post('/',response_model=RoleModelOut)
@check_is_staff_or_permission
async def add_role( 
    role: RoleModel,
    current_user=Depends(get_current_user)
):
    await roleCtrl.roleCrud.set_unique([('role',1)])
    new_role = await roleCtrl.roleCrud.add(role.dict())
    return new_role

# @router.put('/{id_role}/update_permission')
# @check_is_staff_or_permission
# async def update_role(
#   
#     id_role: str,
#     role: UpdateRoleModel,
#     current_user=Depends(get_current_user)
# ):
#     
#     await roleCtrl.roleCrud.update(value=id_role, config_data=role.dict())
#     return {'detail':'Update successfully'}

@router.put('/{id_role}/update_role_user')
@check_is_staff_or_permission
async def update_role( 
    id_role: str, 
    data: UpdateRoleModel,
    current_user=Depends(get_current_user)
):
    await roleCtrl.update_role(id_role, data)
    return {'detail':'Update successfully'}


@router.delete('/{id_role}')
@check_is_staff_or_permission
async def delete_role( 
    id_role: str, 
    current_user=Depends(get_current_user)
):
    await roleCtrl.delete_role(id_role)
    return {'detail','delete successfully'}