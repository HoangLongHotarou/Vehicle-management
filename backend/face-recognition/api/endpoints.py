from fastapi import APIRouter
from .routes.face_recognition import router as face_recognition_router


router = APIRouter(prefix='/api/v1/face-recognition',responses={'404':{'description':'Not found test'}})
router.include_router(face_recognition_router)