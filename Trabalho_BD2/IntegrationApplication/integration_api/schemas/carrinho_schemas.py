# carrinho_schemas.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class ItemCarrinhoSchema(BaseModel):
    id_item: int = Field(..., description="ID do item no sistema")
    nome: str = Field(..., description="Nome do item", max_length=100)
    preco: float = Field(..., description="Preço unitário do item", gt=0)
    quantidade: int = Field(1, description="Quantidade do item", gt=0)
    observacoes: str | None = Field(None, description="Observações sobre o item", max_length=200)


class CarrinhoCreateSchema(BaseModel):
    itens: list[ItemCarrinhoSchema] = Field(default_factory=list, description="Lista de itens no carrinho")


class CarrinhoUpdateSchema(BaseModel):
    itens: list[ItemCarrinhoSchema] = Field(..., description="Lista atualizada de itens no carrinho")


class CarrinhoOutSchema(BaseModel):
    id_carrinho: int = Field(..., description="ID do carrinho")
    id_usuario: int = Field(..., description="ID do usuário dono do carrinho")
    itens: list[ItemCarrinhoSchema] = Field(..., description="Itens no carrinho")
    data_criacao: datetime = Field(..., description="Data de criação do carrinho")
    data_atualizacao: datetime = Field(..., description="Data da última atualização")

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        },
        json_schema_extra={
            "example": {
                "id_carrinho": 1,
                "id_usuario": 123,
                "itens": [
                    {
                        "id_item": 456,
                        "nome": "Hambúrguer Especial",
                        "preco": 25.90,
                        "quantidade": 2,
                        "observacoes": "Sem cebola"
                    }
                ],
                "data_criacao": "2023-01-01T12:00:00",
                "data_atualizacao": "2023-01-01T12:30:00"
            }
        }
    )