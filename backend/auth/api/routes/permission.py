from fastapi import APIRouter

router = APIRouter(prefix='/permissions',tags=['Permission'],responses={404: {'description': 'Not found'}})

@router.get('/')
async def get_all_permission():
    return [
        'get_all_user',
        'get_user',
        'update_user',
        'delete_user',
        'get_all_roles',
        'get_role',
        'add_role',
        'update_role',
        'delete_role'
    ]