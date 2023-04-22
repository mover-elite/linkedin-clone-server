from fastapi import APIRouter
from app.core.config import settings
from app.api.auth import router as auth_router
from datetime import datetime

router = APIRouter(prefix=settings.API_V1_STR)


@router.get("/")
def get_home():
    return {"server_time": datetime.now()}


router.include_router(auth_router)
