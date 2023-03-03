from fastapi import APIRouter
from . import advert_v1

router = APIRouter(prefix="/advert")


router.include_router(advert_v1.router)