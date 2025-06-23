from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.v1 import validator


class ClienteBase(BaseModel):
    Id_cliente: int
    Primeiro_nome_client: str
    Ultimo_nome_client: str
    Data_nascimento_client: date
    CPF_client: str
    Telefone_client: str
    E_mail_client: EmailStr
    Genero_client: str
    E_intolerante_lactose: bool = False
    E_celiaco: bool = False
    E_vegetariano: bool = False
    E_vegano: bool = False

class ClienteCreate(ClienteBase):
    Senha_cliente: str

    @validator('CPF_client')
    def validate_cpf(cls, v):
        if not v.isdigit() or len(v) != 11:
            raise ValueError('CPF deve conter exatamente 11 dígitos numéricos')
        return v

class ClienteUpdate(BaseModel):
    Primeiro_nome_client: Optional[str] = None
    Ultimo_nome_client: Optional[str] = None
    Data_nascimento_client: Optional[date] = None
    Telefone_client: Optional[str] = None
    E_mail_client: Optional[EmailStr] = None
    Genero_client: Optional[str] = None
    E_intolerante_lactose: Optional[bool] = None
    E_celiaco: Optional[bool] = None
    E_vegetariano: Optional[bool] = None
    E_vegano: Optional[bool] = None
    Senha_cliente: Optional[str] = None

class ClienteOut(ClienteBase):
    Id_cliente: int
    Data_cadastro_client: datetime

    class Config:
        orm_mode = True