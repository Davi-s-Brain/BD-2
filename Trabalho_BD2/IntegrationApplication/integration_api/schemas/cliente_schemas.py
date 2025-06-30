from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import date, datetime
from typing import Optional
import re

class ClienteCreate(BaseModel):
    Id_cliente: int
    Primeiro_nome_client: str = Field(..., max_length=50)
    Ultimo_nome_client: str = Field(..., max_length=50)
    Data_nascimento_client: date
    CPF_client: int = Field(...)
    Telefone_client: int = Field(...)
    E_mail_client: EmailStr
    Genero_client: str = Field(..., max_length=10)
    Senha_cliente: str = Field(..., min_length=8, max_length=20)
    E_intolerante_lactose: bool
    E_celiaco: bool
    E_vegetariano: bool
    E_vegano: bool


class ClienteUpdate(BaseModel):
    Primeiro_nome_client: Optional[str] = Field(None, max_length=50)
    Ultimo_nome_client: Optional[str] = Field(None, max_length=50)
    Telefone_client: Optional[str] = Field(None, min_length=10, max_length=11)
    Genero_client: Optional[str] = Field(None, max_length=10)
    Senha_cliente: Optional[str] = Field(None, min_length=8, max_length=20)
    E_intolerante_lactose: Optional[bool] = None
    E_celiaco: Optional[bool] = None
    E_vegetariano: Optional[bool] = None
    E_vegano: Optional[bool] = None

    @field_validator('Telefone_client')
    def validate_telefone(cls, v):
        if v and not v.isdigit():
            raise ValueError('Telefone deve conter apenas números')
        return v

class ClienteOut(BaseModel):
    Id_cliente: int | None
    Primeiro_nome_client: str
    Ultimo_nome_client: str
    Data_nascimento_client: date
    CPF_client: int | None
    Telefone_client: int
    E_mail_client: str
    Data_cadastro_client: date
    Genero_client: str
    E_intolerante_lactose: bool
    E_celiaco: bool
    E_vegetariano: bool
    E_vegano: bool
    Senha_cliente: str

    @field_validator('Data_cadastro_client', mode='before')
    def convert_datetime(cls, value):
        if isinstance(value, datetime):
            return value.date()
        return value
class ClientePass(ClienteOut):
    pass