from api.models.region import (RegionModel, RegionModelListOut, RegionModelOut,
                               UpdateRegionModel)
from fastapi import APIRouter, Query
from utils.pagination import pagination_info
from api.controllers.region import RegionController

router = APIRouter(
    prefix='/regions',
    tags=['Region'],
    responses={404: {'description': 'Not found'}}
)

@router.get('/', response_model=RegionModelListOut)
async def get_all_region(
    page: int = Query(0, ge=0),
    limit: int = Query(0, ge=0, le=10)
):
    regionCtrl = RegionController()
    regions,info = await regionCtrl.regionCrud.get_all(is_get_info=True)
    return pagination_info(regions, info)

@router.get('/{id_region}', response_model=RegionModel)
async def get_region(id_region: str):
    regionCtrl = RegionController()
    region = await regionCtrl.regionCrud.get(value=id_region)
    return region

@router.put('/{id_region}')
async def update_region( id_region: str, data: UpdateRegionModel):
    regionCtrl = RegionController()
    await regionCtrl.regionCrud.update(value=id_region, config_data=data.dict())
    return {'detail': 'Update successfully'}

@router.post('/',response_model=RegionModelOut)
async def add_region( data: RegionModel):
    regionCtrl = RegionController()
    new_region = await regionCtrl.add_region(data.dict())
    return new_region