from typing import Optional

from pydantic import BaseModel

class CreateOrder(BaseModel):
    name: str
    id: int
    product: str
    quantity: int