from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class FuncionarioBase(BaseModel):
    Id_func : str = Field (..., example= 1)
    Nome_func: str = Field(..., example="João Silva")
    CPF: str = Field(..., example="123.456.789-00")
    Data_nasc_func: date = Field(..., example="1990-05-20")
    Cargo: str = Field(..., example="Atendente")
    Salario: float = Field(..., example=2500.50)
    Data_admissao: date = Field(..., example="2024-01-15")
    Turno: str = Field(..., example="Manhã")
    Tipo_de_contrato: str = Field(..., example="CLT")
    Status_func: str = Field(..., example="Ativo")
    Id_franquia: Optional[int] = Field(None, example=1)
    Senha_func: Optional[str] = Field(None, example="senha")

class FuncionarioCreate(FuncionarioBase):
    """Schema para criação de funcionário (Id_func é gerado pelo BD)."""
    pass

class FuncionarioUpdate(BaseModel):
    """Schema para atualização parcial de funcionário."""
    Id_func : Optional[str] = None
    Nome_func: Optional[str] = None
    CPF: Optional[str] = None
    Data_nasc_func: Optional[date] = None
    Cargo: Optional[str] = None
    Salario: Optional[float] = None
    Data_admissao: Optional[date] = None
    Turno: Optional[str] = None
    Tipo_de_contrato: Optional[str] = None
    Status_func: Optional[str] = None
    Id_franquia: Optional[int] = None
    Senha_func: Optional[str] = None


class FuncionarioOut(FuncionarioBase):
    """Schema de saída de funcionário, inclui o Id_func."""
    Id_func: int = Field(..., example=1)

    class Config:
        orm_mode = True