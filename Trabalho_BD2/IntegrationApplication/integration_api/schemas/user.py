from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
class UserLogin(UserBase):
    password: str

class User(UserBase):
    disabled: Optional[bool] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    password: Optional[str] = Field(None, min_length=6, max_length=100)


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True