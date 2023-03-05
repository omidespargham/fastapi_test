from pydantic import BaseModel
from datetime import datetime
from typing import List
from fastapi import Body

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