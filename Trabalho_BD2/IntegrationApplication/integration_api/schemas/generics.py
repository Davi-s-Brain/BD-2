from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
import re

# Schema base para cliente
class ClienteBase(BaseModel):
    Primeiro_nome_client: str = Field(..., max_length=50, example="João")
    Ultimo_nome_client: str = Field(..., max_length=50, example="Silva")
    Data_nascimento_client: date = Field(..., example="1990-05-20")
    CPF_client: int = Field(..., example=12345678901)
    Telefone_client: int = Field(..., example=11999999999)
    E_mail_client: str = Field(..., max_length=50, example="joao@example.com")
    Genero_client: str = Field(..., max_length=10, example="Masculino")
    E_intolerante_lactose: bool = Field(False)
    E_celiaco: bool = Field(False)
    E_vegetariano: bool = Field(False)
    E_vegano: bool = Field(False)

    @validator('CPF_client')
    def validate_cpf(cls, v):
        if len(str(v)) != 11:
            raise ValueError('CPF deve conter exatamente 11 dígitos')
        return v

    @validator('Telefone_client')
    def validate_phone(cls, v):
        if len(str(v)) not in (10, 11):
            raise ValueError('Telefone deve conter 10 ou 11 dígitos')
        return v

class ClienteCreate(ClienteBase):
    Senha_cliente: str = Field(..., min_length=6, max_length=20, example="senha123")

class ClienteUpdate(BaseModel):
    Primeiro_nome_client: Optional[str] = Field(None, max_length=50)
    Ultimo_nome_client: Optional[str] = Field(None, max_length=50)
    Data_nascimento_client: Optional[date] = None
    Telefone_client: Optional[int] = None
    E_mail_client: Optional[str] = Field(None, max_length=50)
    Genero_client: Optional[str] = Field(None, max_length=10)
    E_intolerante_lactose: Optional[bool] = None
    E_celiaco: Optional[bool] = None
    E_vegetariano: Optional[bool] = None
    E_vegano: Optional[bool] = None
    Senha_cliente: Optional[str] = Field(None, min_length=6, max_length=20)

class ClienteOut(ClienteBase):
    Id_cliente: int = Field(..., example=1)
    Data_cadastro_client: date = Field(..., example="2023-06-15")

    class Config:
        orm_mode = True

# Schema para Funcionário
class FuncionarioBase(BaseModel):
    Nome_func: str = Field(..., max_length=50, example="Maria Souza")
    CPF: int = Field(..., example=98765432109)
    Data_nasc_func: date = Field(..., example="1985-08-15")
    Cargo: str = Field(..., max_length=20, example="Gerente")
    Salario: float = Field(..., example=5000.0)
    Data_admissao: date = Field(..., example="2020-01-10")
    Turno: str = Field(..., max_length=20, example="Tarde")
    Tipo_de_contrato: str = Field(..., max_length=20, example="CLT")
    Status_func: str = Field(..., max_length=20, example="Ativo")
    Id_franquia: int = Field(..., example=1)
    E_mail_func: str = Field(..., max_length=50, example="maria@empresa.com")

    @validator('CPF')
    def validate_cpf(cls, v):
        if len(str(v)) != 11:
            raise ValueError('CPF deve conter exatamente 11 dígitos')
        return v

class FuncionarioCreate(FuncionarioBase):
    Senha_func: str = Field(..., min_length=6, max_length=20, example="senha456")

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
    Senha_func: Optional[str] = Field(None, min_length=6, max_length=20)

class FuncionarioOut(FuncionarioBase):
    Id_func: int = Field(..., example=1)

    class Config:
        orm_mode = True

# Schema para Pedido
class PedidoBase(BaseModel):
    Data_pedido: date = Field(..., example="2023-06-15")
    Hora_pedido: str = Field(..., max_length=5, example="14:30")
    Valor_total_pedido: float = Field(..., example=75.50)
    Forma_pagamento: str = Field(..., max_length=20, example="Cartão")
    E_delivery: bool = Field(..., example=True)
    Observacao: str = Field(..., max_length=200, example="Sem cebola")
    Id_func: int = Field(..., example=1)
    Id_cliente: int = Field(..., example=1)

    @validator('Hora_pedido')
    def validate_hora(cls, v):
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', v):
            raise ValueError('Formato de hora inválido. Use HH:MM')
        return v

class PedidoCreate(PedidoBase):
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
    Id_pedido: int = Field(..., example=1)

    class Config:
        orm_mode = True

# Schema para Produto
class ProdutoBase(BaseModel):
    Nome_prod: str = Field(..., max_length=50, example="Hambúrguer")
    Preco_prod: float = Field(..., example=15.99)
    Peso_prod: float = Field(..., example=0.3)
    Unidade_medida: str = Field(..., max_length=2, example="kg")
    Restricao_alimentar: str = Field(..., max_length=50, example="Contém glúten")
    Categoria: str = Field(..., max_length=50, example="Lanche")

class ProdutoCreate(ProdutoBase):
    Sobremesa: Optional[bool] = None
    Lanche: Optional[bool] = None
    Bebida: Optional[bool] = None
    Acompanhamento: Optional[bool] = None

class ProdutoUpdate(BaseModel):
    Nome_prod: Optional[str] = Field(None, max_length=50)
    Preco_prod: Optional[float] = None
    Peso_prod: Optional[float] = None
    Unidade_medida: Optional[str] = Field(None, max_length=2)
    Restricao_alimentar: Optional[str] = Field(None, max_length=50)
    Categoria: Optional[str] = Field(None, max_length=50)
    Sobremesa: Optional[bool] = None
    Lanche: Optional[bool] = None
    Bebida: Optional[bool] = None
    Acompanhamento: Optional[bool] = None

class ProdutoOut(ProdutoBase):
    Indice_prod: int = Field(..., example=1)
    Sobremesa: Optional[bool] = None
    Lanche: Optional[bool] = None
    Bebida: Optional[bool] = None
    Acompanhamento: Optional[bool] = None

    class Config:
        orm_mode = True

# Schema para Franquia
class FranquiaBase(BaseModel):
    Nome_franquia: str = Field(..., max_length=50, example="FastBurger Ibirapuera")
    CNPJ: int = Field(..., example=12345678000199)
    Endereco_franq: str = Field(..., max_length=50, example="Av. Ibirapuera, 1000")
    E_mail_franq: str = Field(..., max_length=50, example="contato@fastburger.com")
    Data_inauguracao_franq: date = Field(..., example="2020-05-10")

    @validator('CNPJ')
    def validate_cnpj(cls, v):
        if len(str(v)) != 14:
            raise ValueError('CNPJ deve conter exatamente 14 dígitos')
        return v

class FranquiaCreate(FranquiaBase):
    pass

class FranquiaUpdate(BaseModel):
    Nome_franquia: Optional[str] = Field(None, max_length=50)
    CNPJ: Optional[int] = None
    Endereco_franq: Optional[str] = Field(None, max_length=50)
    E_mail_franq: Optional[str] = Field(None, max_length=50)
    Data_inauguracao_franq: Optional[date] = None

class FranquiaOut(FranquiaBase):
    Id_franquia: int = Field(..., example=1)

    class Config:
        orm_mode = True

class ItemDisponibilidade(BaseModel):
    item: str
    quantidade_estoque: float
    mensagem: str

class ComboDisponibilidadeRequest(BaseModel):
    id_lanche: Optional[int] = None
    id_bebida: Optional[int] = None
    id_sobremesa: Optional[int] = None
    id_acompanhamento: Optional[int] = None

class ComboDisponibilidadeResponse(BaseModel):
    itens: List[ItemDisponibilidade]
    status_geral: str
    disponivel: bool
    timestamp: datetime = datetime.now()