from sqlalchemy.orm import Session
from models.user_model import UserDB, RGScode
from models.advert_models import Category
from fastapi import HTTPException
import schema


def check_parent_category_and_category_unique_name(parent_id,category_name,db:Session):
    if not db.query(Category).filter(Category.name == category_name).first():
        parent_category = db.query(Category).filter(Category.id == parent_id).first()
        if parent_category:
            return parent_category.id
    else:
        raise HTTPException(status_code=404,detail="category with this name exist !")
    return None



