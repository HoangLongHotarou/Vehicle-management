from fastapi import APIRouter

router = APIRouter(prefix='/permissions',tags=['Permission'],responses={404: {'description': 'Not found'}})

@router.get('/')
async def get_permission():
    return [
        'get_all_vehicle',
        'get_vehicle',
        'add_vehicle',
        'update_vehicle',
        'delete_vehicle'
    ]