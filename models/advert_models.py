from db.database import Base
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
# from .user_model import UserDB

# NOTE: turn off server if you want to make models


class Advert(Base):
    __tablename__ = "adverts"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String) # make the validation for max_lenght 50
    description = Column(String)
    price = Column(String)
    price2 = Column(String)
    phone_number = Column(String)
    user_id = Column(Integer,ForeignKey("users.id"))
    user = relationship("UserDB",back_populates="adverts")

class Category(Base):
    __tablename__ = "categorys"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,unique=True)
    parent_id = Column(Integer,ForeignKey("categorys.id"))
    # category_type = # this should be a choise for catgory type