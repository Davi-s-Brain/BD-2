from pydantic import BaseModel
from typing import Optional
from datetime import date, time

# Schema para criação de pedidos (sem ID)
class PedidoCreate(BaseModel):
    Data_pedido: date
    Hora_pedido: time
    Valor_total_pedido: float
    Forma_pagamento: str
    E_delivery: bool
    Observacao: Optional[str]
    Id_cliente: int
    Id_func: int

# Schema para atualização de pedidos (campos opcionais)
class PedidoUpdate(BaseModel):
    Data_pedido: Optional[date] = None
    Hora_pedido: Optional[time] = None
    Valor_total_pedido: Optional[float] = None
    Forma_pagamento: Optional[str] = None
    E_delivery: Optional[bool] = None
    Observacao: Optional[str] = None
    Id_cliente: Optional[int] = None
    Id_func: Optional[int] = None

# Schema para leitura (retorno ao usuário), inclui o ID
class PedidoOut(BaseModel):
    Id_pedido: int
    Data_pedido: date
    Hora_pedido: time
    Valor_total_pedido: float
    Forma_pagamento: str
    E_delivery: bool
    Observacao: Optional[str]
    Id_cliente: int
    Id_func: int

    class Config:
        orm_mode = True  # Permite compatibilidade com ORM ou sqlite3.Row

