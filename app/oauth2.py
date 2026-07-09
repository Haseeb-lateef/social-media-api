from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")#extracts token

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES =  60


def create_token(data: dict):
    to_encode = data.copy()
    expire =  datetime.now(timezone.utc) +  timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    print(expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError as e:
        print(e)
        raise credentials_exception
    
    return token_data


def get_current_user(token: str =Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exceptions = HTTPException( status_code= status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials", headers={"www-Authenticate": "Bearer"})

    token = verify_token(token,credentials_exceptions)

    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user


