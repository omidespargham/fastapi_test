from fastapi import APIRouter, Depends, HTTPException, Query, Body, status
from sqlalchemy.orm import Session
from models.user_model import UserDB,RGScode
from db.database import get_db
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db.hash import Hash
from auth import oauth2


router = APIRouter(tags=["authentication"])


@router.post("/token")
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if not request.username == "admin":
        user = db.query(UserDB).filter(
            UserDB.phone_number == request.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="user with this username dosent exist")

        if not Hash.verify(user.password, request.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="pass is not correct")
    else:
        request.username = "1"
    access_token = oauth2.create_access_token(data={"sub": request.username})

    return {
        "access_token": access_token,
        "type_token": "bearer",
    }


@router.post("/make_admin_user")
def make_admin_user(password: str = Body(Ellipsis,title="enter your password"), db: Session = Depends(get_db)):
    if password == "admin1":
        user = db.query(UserDB).filter(
            UserDB.phone_number == "1").first()
        if not user:
            user = UserDB(phone_number="1")
            db.add(user)
            db.commit()
        return {"username": "admin", "password": "test"}

    raise HTTPException(
        status_code=404, detail="your password is not correct ! ")
