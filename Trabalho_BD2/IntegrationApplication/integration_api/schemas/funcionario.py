from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

from pydantic.v1 import validator


class FuncionarioBase(BaseModel):
    Id_func : int | None = Field (..., example= 1)
    Nome_func: str = Field(..., example="João Silva")
    CPF: int = Field(..., example="123.456.789-00")
    Data_nasc_func: date = Field(..., example="1990-05-20")
    Cargo: str = Field(..., example="Atendente")
    Salario: float = Field(..., example=2500.50)
    Data_admissao: date = Field(..., example="2024-01-15")
    Turno: str = Field(..., example="Manhã")
    Tipo_de_contrato: str = Field(..., example="CLT")
    Status_func: str = Field(..., example="Ativo")
    Id_franquia: Optional[int] = Field(None, example=1)
    Senha_Func: Optional[str] = Field(None, example="senha")

class FuncionarioCreate(FuncionarioBase):
    pass

class FuncionarioUpdate(BaseModel):
    Nome_func: Optional[str] = Field(None, max_length=50)
    CPF: Optional[int] = None
    Data_nasc_func: Optional[date] = None
    Cargo: Optional[str] = Field(None, max_length=20)
    Salario: Optional[float] = None
    Data_admissao: Optional[date] = None
    Turno: Optional[str] = Field(None, max_length=20)
    Tipo_de_contrato: Optional[str] = Field(None, max_length=20)
    Status_func: Optional[str] = Field(None, max_length=20)
    Id_franquia: Optional[int] = None
    E_mail_func: Optional[str] = Field(None, max_length=50)
    Senha_Func: Optional[str] = Field(None, min_length=6, max_length=20)

class FuncionarioOut(FuncionarioBase):
    class Config:
        orm_mode = True