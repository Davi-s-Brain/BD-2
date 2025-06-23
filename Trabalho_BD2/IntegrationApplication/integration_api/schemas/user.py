from typing import Optional
from pydantic import BaseModel

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