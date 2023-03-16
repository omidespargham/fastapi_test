from pydantic import BaseModel,Field,validator
from datetime import datetime
from typing import List,Optional,Union
from fastapi import Body,Depends,HTTPException
from db.database import get_db
from sqlalchemy.orm import Session
from models.advert_models import Category
# sub schemas ######################################################


# user schemas ######################################################


class UserBase(BaseModel):
    phone_number:str = Body(Ellipsis,regex="^09\d{3}$")# validate if it is 11 char and start with 09

class UserShow(UserBase):
    id:int

class UserVerify(BaseModel):
    code:int = Body(Ellipsis,ge=10000,le=99999)



# advert schemas ######################################################


class AdvertBase(BaseModel):
    title:str
    description:str
    price:str
    phone_number:str
    user_id:int

class AdvertShow(AdvertBase):
    id:int

    class Config:
        orm_mode = True


# category schemas ######################################################


class CategoryBase(BaseModel):
    name:str
    parent_id:Optional[int] = Field(None)

    # @validator('name')
    # def name_of_category_should_be_unique(cls,v,value):
    #     # check_the_category_unique(value,db = get_db())
    #     return v
class CategoryParentShow(CategoryBase):
    id:int

class CategoryShow(CategoryBase):
    id:int
    parent:Union[CategoryParentShow,None,list]
    class Config:
        orm_mode = True
