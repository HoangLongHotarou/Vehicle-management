from fastapi import APIRouter

from .routes.auth import router as auth_router
from .routes.in_and_out import router as in_and_out_router
from .routes.permission import router as permission_router
from .routes.region import router as region_router
from .routes.vehicle import router as vehicle_router

router = APIRouter(prefix='/api/v1/license-plate-app',responses={'404':{'description':'Not found test'}})
router.include_router(permission_router)
router.include_router(auth_router)
router.include_router(vehicle_router)
router.include_router(region_router)
router.include_router(in_and_out_router)