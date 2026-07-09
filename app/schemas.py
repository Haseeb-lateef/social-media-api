
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):

    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr

    class Config:
        from_attributes = True



class PostReponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    password: str
    email: EmailStr






    class Config:
        from_attributes = True


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):

    id: Optional[int] = None










