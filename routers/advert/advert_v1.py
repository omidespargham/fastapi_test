from fastapi import APIRouter, Depends, Body, HTTPException
from typing import List
import schema
from sqlalchemy.orm import Session
from db.database import get_db
from db import user_db, advert_db
from models.user_model import RGScode, UserDB
from models.advert_models import Advert, Category
from auth.oauth2 import create_access_token

router = APIRouter(prefix="/v1", tags=["advert_v1"])


@router.post("/make-advert", response_model=schema.AdvertShow)
def make_advert(request: schema.AdvertBase, db: Session = Depends(get_db)):
    advert = Advert(title=request.title, description=request.description, price=request.price,
                    user_id=request.user_id, phone_number=request.phone_number)
    db.add(advert)
    db.commit()
    db.refresh(advert)
    return advert


@router.get("/get_all_adverts/{user_id}", response_model=List[schema.AdvertShow])
def get_all_adverts(user_id: int, db: Session = Depends(get_db)):
    adverts = db.query(Advert).filter(Advert.user_id == user_id).all()
    return adverts


@router.get("/advert-detail/{advert_id}", response_model=schema.AdvertShow)
def advert_detail(advert_id: int, db: Session = Depends(get_db)):
    advert = db.query(Advert).filter(Advert.id == advert_id).first()
    if not advert:
        raise HTTPException(
            status_code=404, detail="advert with this id didnt exist !")
    return advert


@router.post("/make_category", response_model=schema.CategoryShow)
def make_category(request: schema.CategoryBase, db: Session = Depends(get_db)):
    parent_id = advert_db.check_parent_category_and_category_unique_name(
        request.parent_id, request.name, db)
    category = Category(name=request.name,
                        parent_id=parent_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.post("/get_category/{category_id}",response_model=schema.CategoryShow)
def get_category(category_id,db:Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404,detail="category with this id didnt exist")
    return category
