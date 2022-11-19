from fastapi import APIRouter

from .routes.permission import router as permission_router
from .routes.role import router as role_router
from .routes.user import router as user_router

router = APIRouter(prefix='/api/v1/auth',responses={'404':{'description':'Not found'}})
router.include_router(user_router)
router.include_router(permission_router)
router.include_router(role_router)
