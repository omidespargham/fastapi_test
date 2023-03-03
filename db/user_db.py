import random
import string
from sqlalchemy.orm import Session
from models.user_model import UserDB, RGScode
from fastapi import HTTPException
import schema
from random import randint


def get_random_string():
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(10))
    return result_str


def get_user_by_phone_number(phone_number: str, db: Session):
    user = db.query(UserDB).filter(UserDB.phone_number == phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found !")
    return user


def make_rgs_code(phone_number, db: Session):
    # if phone_number[0:2] != "09":
    #     raise HTTPException(status_code=404, detail="تلفن باید با 09 شروع شود")
    last_rgs_code = db.query(RGScode).filter(RGScode.phone_number == phone_number).first()
    if last_rgs_code:
        db.delete(last_rgs_code)
    the_code = randint(10000, 99999)
    rgs = RGScode(code=the_code, phone_number=phone_number)
    db.add(rgs)
    db.commit()
    db.refresh(rgs)
    return rgs
