from .. import models, schemas, utility
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix= "/users",
    tags=["Users"]
)




@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    

    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail=f"the email:{user.email} already exists")
    

    user.password = utility.hash_password(user.password)

    new_user = models.Users(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get("/{id}", response_model= schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    result = db.query(models.Users).filter(models.Users.id == id).first()


    if not result:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="user not found")
    
    return result