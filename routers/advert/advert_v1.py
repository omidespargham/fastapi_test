from fastapi import APIRouter, Depends, Body, HTTPException
from typing import List
import schema
from sqlalchemy.orm import Session
from db.database import get_db
from db import user_db
from models.user_model import RGScode, UserDB
from auth.oauth2 import create_access_token

router = APIRouter(prefix="/v1", tags=["advert_v1"])


