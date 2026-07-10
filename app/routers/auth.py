from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utility, oauth2, schemas
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(tags= ["Authentication"])
#tags just defines a name for the router



@router.post("/login", response_model= schemas.Token)
#pulls username and pass from http request()
def login(login_info: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == login_info.username).first()
    print(user)
    print(login_info.username)
    print(login_info.password)

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Invalid credential")
    
    if not utility.verify(login_info.password,user.password):

        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Invalid credential")
    
    access_token = oauth2.create_token(data = {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


        

