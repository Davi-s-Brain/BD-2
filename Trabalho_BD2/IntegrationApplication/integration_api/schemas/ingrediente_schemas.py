from pydantic import BaseModel, Field
from typing import Optional

class IngredienteBase(BaseModel):
    Tipo_ingred: str = Field(..., example="Proteína")
    Nome_ingred: str = Field(..., example="Hambúrguer de Carne")
    Preco_venda_cliente: float = Field(..., example=12.50)
    Peso_ingred: float = Field(..., example=180.0)
    Indice_estoq: int = Field(..., example=1)
    Quantidade: int = Field(..., example=1)

class IngredienteCreate(IngredienteBase):
    """Schema para criação de ingrediente (Id_ingred é gerado pelo BD)."""
    pass

class IngredienteUpdate(BaseModel):
    """Schema para atualização parcial de ingrediente."""
    Tipo_ingred: Optional[str] = None
    Nome_ingred: Optional[str] = None
    Preco_venda_cliente: Optional[float] = None
    Peso_ingred: Optional[float] = None
    Indice_estoq: Optional[int] = None
    Quantidade: int

class IngredienteOut(IngredienteBase):
    """Schema de saída de ingrediente, inclui o Id_ingred."""
    Id_ingred: int = Field(..., example=1)

    class Config:
        orm_mode = True