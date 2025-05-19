from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int
    value : int

class ItemUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int
    value: int

class ItemOut(BaseModel):
    name: str
    description: str
    quantity: int
    value: int
