# schemas/ambiente.py
from pydantic import BaseModel
from typing import Optional

class AmbienteBase(BaseModel):
    Id_franquia: int
    Tamanho_ambiente: float
    Quantidade_desse_ambiente: float
    Nivel_limpeza: str
    Detetizado: bool
    Salao: Optional[bool] = None
    Cozinha: Optional[bool] = None

class AmbienteCreate(AmbienteBase):
    pass

class Ambiente(AmbienteBase):
    Id_Amb: int

    class Config:
        orm_mode = True