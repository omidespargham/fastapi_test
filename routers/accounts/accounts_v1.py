from fastapi import APIRouter, Depends, Body, HTTPException
from typing import List
import schema
from sqlalchemy.orm import Session
from db.database import get_db
from db import user_db
from . import accounts_v1
from models.user_model import RGScode, UserDB
from auth.oauth2 import create_access_token

router = APIRouter(prefix="/v1", tags=["accounts_v1"])


@router.post("/login")
def login(request: schema.UserBase, db: Session = Depends(get_db)):
    rgs = user_db.make_rgs_code(request.phone_number, db)
    return {
        "phone_number": request.phone_number,
        "code": rgs.code}


@router.post("/login_verify")
def login_verify(request: schema.UserVerify, db: Session = Depends(get_db)):
    rgs = db.query(RGScode).filter(RGScode.code == request.code).first()
    if not rgs:
        raise HTTPException(
            status_code=404, detail="کد وجود ندارد و یا منقضی شده")
    phone = rgs.phone_number
    db.delete(rgs)
    user = db.query(UserDB).filter(UserDB.phone_number == phone).first()
    if not user:
        user = UserDB(phone_number=phone, password=user_db.get_random_string())
        db.add(user)
        # db.refresh(user)
    db.commit()
    user_token = create_access_token(data={"sub": user.phone_number})

    return {
        "access_token": user_token,
        "type_token": "bearer",
    }
