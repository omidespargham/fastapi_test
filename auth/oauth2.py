from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import timedelta,datetime
from jose import jwt,JWTError
from fastapi import Depends,HTTPException
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.user_db import get_user_by_phone_number

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = 'c4a4ba25aa53cdfc7bd6f6e5451464ada76957fc3d238ae104842eb806619b87'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict,expires_delta: Optional[timedelta]= None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.Utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token:str =Depends(oauth_scheme),db:Session = Depends(get_db)):
    error_credential = HTTPException(status_code=401,detail="invalid credentials",
                                     headers={"WWW-authenticate":"bearer"})
    
    try:
        _dict = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        phone_number = _dict.get("sub")
        if not phone_number:
            raise error_credential
    except JWTError:
        raise error_credential
    
    user = get_user_by_phone_number(phone_number,db)

    return user
