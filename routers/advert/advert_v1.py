from fastapi import APIRouter, Depends, Body, HTTPException
from typing import List
import schema
from sqlalchemy.orm import Session
from db.database import get_db
from db import user_db
from models.user_model import RGScode, UserDB
from models.advert_models import Advert
from auth.oauth2 import create_access_token

router = APIRouter(prefix="/v1", tags=["advert_v1"])


@router.post("/make-advert",response_model=schema.AdvertShow)
def make_advert(request:schema.AdvertBase,db:Session=Depends(get_db)):
    advert = Advert(title=request.title,description=request.description,price=request.price,
                    user_id=request.user_id,phone_number=request.phone_number)
    db.add(advert)
    db.commit()
    db.refresh(advert)
    return advert

@router.get("/get_all_adverts/{user_id}",response_model=List[schema.AdvertShow])
def get_all_adverts(user_id:int,db:Session = Depends(get_db)):
    adverts = db.query(Advert).filter(Advert.user_id == user_id).all()
    return adverts