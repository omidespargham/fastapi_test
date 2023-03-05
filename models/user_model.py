from db.database import Base
from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import relationship
# from .advert_models import Advert



class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    phone_number = Column(String,unique=True)
    password = Column(String)
    adverts = relationship("Advert",back_populates="user")

class RGScode(Base):
    __tablename__ = "rgs_codes"
    id = Column(Integer,primary_key=True,index=True)
    code = Column(Integer)
    phone_number = Column(String)
    