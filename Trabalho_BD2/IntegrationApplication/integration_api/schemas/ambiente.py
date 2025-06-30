from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class AmbienteBaseSchema(BaseModel):
    Id_franquia: int = Field(..., description="ID da franquia a que o ambiente pertence")
    Tamanho_ambiente: float = Field(..., gt=0, description="Tamanho do ambiente em metros quadrados")
    Quantidade_desse_ambiente: float = Field(..., gt=0, description="Quantidade deste tipo de ambiente")
    Nivel_limpeza: str = Field(..., description="Nível de limpeza do ambiente (ex: 'limpo', 'sujo', 'em limpeza')")
    Detetizado: bool = Field(False, description="Indica se o ambiente foi detetizado recentemente")
    Salao: Optional[bool] = Field(None, description="Indica se é um salão")
    Cozinha: Optional[bool] = Field(None, description="Indica se é uma cozinha")

class AmbienteCreateSchema(AmbienteBaseSchema):
    pass

class AmbienteUpdateSchema(BaseModel):
    Tamanho_ambiente: Optional[float] = Field(None, gt=0)
    Quantidade_desse_ambiente: Optional[float] = Field(None, gt=0)
    Nivel_limpeza: Optional[str] = Field(None)
    Detetizado: Optional[bool] = Field(None)
    Salao: Optional[bool] = Field(None)
    Cozinha: Optional[bool] = Field(None)


class AmbienteOutSchema(AmbienteBaseSchema):
    Id_Amb: int | None = Field(..., description="ID único do ambiente")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "Id_Amb": 1,
                "Id_franquia": 10,
                "Tamanho_ambiente": 25.5,
                "Quantidade_desse_ambiente": 2,
                "Nivel_limpeza": "limpo",
                "Detetizado": True,
                "Salao": True,
                "Cozinha": False
            }
        }

class AmbienteListSchema(BaseModel):
    ambientes: List[AmbienteOutSchema] = Field(..., description="Lista de ambientes")

class AmbienteCountByTypeSchema(BaseModel):
    salao: int = Field(..., description="Quantidade de salões")
    cozinha: int = Field(..., description="Quantidade de cozinhas")
    outros: int = Field(..., description="Quantidade de outros tipos de ambiente")

class LimpezaUpdateSchema(BaseModel):
    Nivel_limpeza: str = Field(..., description="Novo nível de limpeza")
    Detetizado: bool = Field(..., description="Indica se foi detetizado")
