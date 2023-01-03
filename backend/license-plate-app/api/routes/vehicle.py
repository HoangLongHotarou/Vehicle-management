import json
from typing import List

from api.models.vehicle import (UpdateVehicleModel, VehicleModel,
                                VehicleModelListOut, VehicleModelOut,
                                VehicleSubModel)
from core.jwt import get_current_user
from fastapi import APIRouter, Depends, File, Query,UploadFile
from utils.decorators import check_has_permission
from utils.pagination import pagination_info
from utils.pyobjectid import PyObjectId
from api.controllers.vehicle import VehicleController

router = APIRouter(
    prefix='/vehicles',
    tags=['Vehicle'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/', response_model=VehicleModelListOut)
# @check_has_permissions
async def get_all_vehicle(
    page: int = Query(0, ge=0),
    limit: int = Query(20, ge=0, le=20),
    # current_user=Depends(get_current_user)
):
    vehicleCtrl = VehicleController()
    vehicles, info = await vehicleCtrl.vehicleCrud.get_all(is_get_info=True, page=page, limit=limit)
    return pagination_info(vehicles, info)


@router.post('/me', response_model=VehicleModelOut)
async def add_vehicle_for_current_user(
    vehicle: VehicleSubModel,
    current_user=Depends(get_current_user)
):
    vehicleCtrl = VehicleController()
    new_data = await vehicleCtrl.add_vehicle_for_current_user(vehicle, current_user['id'])
    return new_data


@router.get('/me', response_model=VehicleModelListOut)
async def get_all_user_vehicle(
    page: int = Query(0, ge=0),
    limit: int = Query(20, ge=0, le=20),
    current_user=Depends(get_current_user)
):
    vehicleCtrl = VehicleController()
    vehicles, info = await vehicleCtrl.vehicleCrud.get_all(
        query={'user_id': PyObjectId(current_user['id'])},
        is_get_info=True,
        page=page,
        limit=limit)
    return pagination_info(vehicles, info)


@router.get('/{id_vehicle}', response_model=VehicleModelOut)
@check_has_permission
async def get_vehicle(
    id_vehicle: str,
    current_user=Depends(get_current_user)
):
    vehicleCtrl = VehicleController()
    vehicle = await vehicleCtrl.vehicleCrud.get(value=id_vehicle)
    return vehicle


@router.post('/', response_model=VehicleModelOut)
@check_has_permission
async def add_vehicle(
    vehicle: VehicleModel,
    current_user=Depends(get_current_user)
):
    vehicleCtrl = VehicleController()
    await vehicleCtrl.vehicleCrud.set_unique([('plate', 1)])
    new_data = await vehicleCtrl.vehicleCrud.add(vehicle.dict())
    return new_data


@router.put('/{id_vehicle}')
@check_has_permission
async def update_vehicle(
    id_vehicle: str,
    update: UpdateVehicleModel,
    current_user=Depends(get_current_user)
):
    vehicleCtrl = VehicleController()
    is_finish = await vehicleCtrl.vehicleCrud.update(id_vehicle, update.dict())
    return {"detail": "update successfully"} if is_finish == True else {"detail": "not to update"}


@router.delete('/{id_vehicle}')
@check_has_permission
async def delete_vehicle(
    id_vehicle: str,
    current_user=Depends(get_current_user)
):
    vehicleCtrl = VehicleController()
    await vehicleCtrl.vehicleCrud.delete(value=id_vehicle)
    return {"detail": "delete successfully"}


@router.post('/read_file_json')
async def read_file_json( upload_file: UploadFile = File(...)):
    vehicleCtrl = VehicleController()
    json_data = json.load(upload_file.file)
    await vehicleCtrl.insert_json(json_data['list'])
    return {"detail": "add json successfully"}
