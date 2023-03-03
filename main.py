from fastapi import FastAPI, Depends
from db.database import engine
from models import user_model
from routers.accounts import accounts
from routers.advert import advert
from auth.oauth2 import oauth_scheme
from auth import authentication
import schema
from auth.oauth2 import get_current_user
app = FastAPI()


user_model.Base.metadata.create_all(engine)
app.include_router(accounts.router)
app.include_router(authentication.router)
app.include_router(advert.router)


@app.get("/")
def Home(current_user: schema.UserShow = Depends(get_current_user)):
    return {current_user.phone_number}
