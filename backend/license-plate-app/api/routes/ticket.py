from api.models.ticket import (TicketUserSchema)
from fastapi import APIRouter, Query, Depends
from utils.pagination import pagination_info
from core.jwt import get_current_user
from api.controllers.controller import *

router = APIRouter(
    prefix='/tickets',
    tags=['Tickets'],
    responses={404: {'description': 'Not found'}}
)

@router.post('/me')
async def add_vehicle_for_current_user(
    ticket_schema: TicketUserSchema,
    current_user=Depends(get_current_user)
):
    await ticketCtrl.add_ticked(ticket_schema.ticket_type,ticket_schema.vehicle_type, current_user['id'])
    return "test"


# @router.get('/me', response_model=VehicleModelListOut)
# async def get_all_user_vehicle(
    
#     page: int = Query(0, ge=0),
#     limit: int = Query(20, ge=0, le=20),
#     current_user=Depends(get_current_user)
# ):
#     vehicles, info = await vehicleCtrl.vehicleCrud.get_all(
#         query={'user_id': PyObjectId(current_user['id'])},
#         is_get_info=True,
#         page=page,
#         limit=limit)
#     return pagination_info(vehicles, info)