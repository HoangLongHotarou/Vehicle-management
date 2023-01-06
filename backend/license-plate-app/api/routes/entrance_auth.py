from fastapi import APIRouter, Query
from utils.pagination import pagination_info
from api.models.entrance_auth import *
from api.models.entrance_auth_region import *
from api.models.entrance_auth_user import *
from api.controllers.entrance_auth import EntranceAuthController

router = APIRouter(
    prefix='/entrance_auth',
    tags=['Entrance Auth'],
    responses={404: {'description': 'Not found'}}
)

@router.get('/',response_model=EntranceAuthListModelOut)
async def get_all_entrance_auth(
    page: int = Query(0,ge=0),
    limit: int = Query(0,ge=0,le=10)
):
    entranceAuthCtrl = EntranceAuthController()
    entrance_auth, info = await entranceAuthCtrl.get_all_entrance_auth(page,limit)
    return pagination_info(entrance_auth, info)

@router.post('/',response_model=EntranceAuthModelOut)
async def add_entrance_auth(data: EntranceAuthModel):
    entranceAuthCtrl = EntranceAuthController()
    entrance_auth = await entranceAuthCtrl.create_entrance_auth(data.dict())
    return entrance_auth

@router.post('/regions',response_model=EntranceAuthRegionModelOut)
async def add_entrance_auth_region(data: EntranceAuthRegionModel):
    entranceAuthCtrl = EntranceAuthController()
    entrance_auth_region = await entranceAuthCtrl.add_entrance_auth_region(data.dict())
    return entrance_auth_region

@router.get('/regions',response_model=EntranceAuthRegionListModelV2Out)
async def get_all_entrance_auth_region(
    page: int = Query(0,ge=0),
    limit: int = Query(10,ge=0,le=10)
):
    entranceAuthCtrl = EntranceAuthController()
    return await entranceAuthCtrl.get_all_entrance_auth_region(page, limit)

@router.delete('/regions/{id}')
async def delete_entrance_auth_region(id: PyObjectId):
    entranceAuthCtrl = EntranceAuthController()
    await entranceAuthCtrl.delete_entrance_auth_region(id)
    return {"detail":"Delete successfully"}

@router.post('/users',response_model=EntranceAuthUserModelOut)
async def add_entrance_auth_user(data: EntranceAuthUserModel):
    entranceAuthCtrl = EntranceAuthController()
    entrance_auth_user = await entranceAuthCtrl.add_entrance_auth_user(data.dict())
    return entrance_auth_user

@router.post('/users/student',response_model=EntranceAuthUserModelOut)
async def add_entrance_auth_user(data: EntranceAuthStudentModel):
    data = {**data.dict(),"id_entrance_auth":PyObjectId("63948266198c29f9c21005fa")}
    entrance_auth_user = await entranceAuthCtrl.add_entrance_auth_user(data)
    return entrance_auth_user

@router.get('/users',response_model=EntranceAuthUserListModelV2Out)
async def get_all_entrance_auth_user(
    page: int = Query(0,ge=0),
    limit: int = Query(10,ge=0,le=10)
):
    entranceAuthCtrl = EntranceAuthController()
    return await entranceAuthCtrl.get_all_entrance_auth_user(page, limit)

@router.delete('/users/{id}')
async def delete_entrance_auth_user(id: PyObjectId):
    entranceAuthCtrl = EntranceAuthController()
    await entranceAuthCtrl.delete_entrance_auth_user(id)
    return {"detail":"Delete successfully"}