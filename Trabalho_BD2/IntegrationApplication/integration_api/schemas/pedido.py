import re

from pydantic import BaseModel, Field, field_validator
from datetime import date, time
from typing import Optional

from pydantic.v1 import validator


class PedidoBase(BaseModel):
    Data_pedido: date = Field(..., example="2023-06-15")
    Hora_pedido: Optional[time] = Field(..., example="14:30")
    Valor_total_pedido: float = Field(..., example=75.50)
    Forma_pagamento: str = Field(..., max_length=20, example="Cartão")
    E_delivery: bool = Field(..., example=True)
    Observacao: str = Field(..., max_length=200, example="Sem cebola")
    Id_func: int = Field(..., example=1)
    Id_cliente: int = Field(..., example=1)

    @validator('Hora_pedido')
    def validate_hora(self, v):
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', v):
            raise ValueError('Formato de hora inválido. Use HH:MM')
        return v

class PedidoCreate(PedidoBase):
    Id_pedido: int | None = Field(..., example=1)
    pass

class PedidoUpdate(BaseModel):
    Data_pedido: Optional[date] = None
    Hora_pedido: Optional[str] = Field(None, max_length=5)
    Valor_total_pedido: Optional[float] = None
    Forma_pagamento: Optional[str] = Field(None, max_length=20)
    E_delivery: Optional[bool] = None
    Observacao: Optional[str] = Field(None, max_length=200)
    Id_func: Optional[int] = None
    Id_cliente: Optional[int] = None

class PedidoOut(PedidoBase):
    Id_pedido: int | None = Field(..., example=1)

    class Config:
        orm_mode = True
