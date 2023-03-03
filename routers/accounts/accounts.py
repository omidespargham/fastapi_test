from fastapi import APIRouter
from . import accounts_v1

router = APIRouter(prefix="/accounts")


router.include_router(accounts_v1.router)