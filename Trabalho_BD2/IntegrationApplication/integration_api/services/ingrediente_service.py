from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from tensorflow.python.keras.layers.core import ClassMethod

from Trabalho_BD2.IntegrationApplication.integration_api.models.ingrediente_model import IngredienteModel
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.ingrediente_schemas import IngredienteCreate, \
    IngredienteOut, IngredienteUpdate


class IngredienteService:
    @staticmethod
    def create(ingrediente_data: IngredienteCreate) -> IngredienteOut:
        """
        Cria um novo ingrediente no banco de dados.

        Args:
            ingrediente_data: Dados do ingrediente a ser criado

        Returns:
            IngredienteOut: Ingrediente criado com ID

        Raises:
            HTTPException: Se ocorrer erro na criação
        """
        try:
            ingrediente = IngredienteModel.create(**ingrediente_data.model_dump())
            if not ingrediente:
                raise ValueError("Falha ao criar ingrediente")
            return IngredienteOut.model_validate(ingrediente.to_dict())
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno ao criar ingrediente: {str(e)}"
            )

    @staticmethod
    def obter_todos() -> List[IngredienteOut]:
        """Retorna todos os ingredientes cadastrados"""
        try:
            ingredientes = IngredienteModel.get_all()
            return [IngredienteOut.model_validate(i.to_dict()) for i in ingredientes]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar ingredientes: {str(e)}"
            )

    @staticmethod
    def obter_por_id(ingrediente_id: int) -> Optional[IngredienteOut]:
        """Obtém um ingrediente pelo seu ID"""
        try:
            ingrediente = IngredienteModel.get_by_id(ingrediente_id)
            if not ingrediente:
                return None
            return IngredienteOut.model_validate(ingrediente.to_dict())
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar ingrediente: {str(e)}"
            )

    @staticmethod
    def atualizar_ingrediente(
            ingrediente_id: int,
            update_data: IngredienteUpdate
    ) -> IngredienteOut:
        """
        Atualiza um ingrediente existente

        Args:
            ingrediente_id: ID do ingrediente a ser atualizado
            update_data: Dados parciais para atualização

        Returns:
            IngredienteOut: Ingrediente atualizado
        """
        try:
            # Remove campos não informados (None)
            update_values = {k: v for k, v in update_data.model_dump().items() if v is not None}

            if not update_values:
                raise ValueError("Nenhum dado válido fornecido para atualização")

            ingrediente = IngredienteModel.get_by_id(ingrediente_id)
            if not ingrediente:
                raise ValueError("Ingrediente não encontrado")

            if not IngredienteModel.update(ingrediente_id, **update_values):
                raise ValueError("Falha ao atualizar ingrediente")

            # Retorna o ingrediente atualizado
            ingrediente_atualizado = IngredienteModel.get_by_id(ingrediente_id)
            return IngredienteOut.model_validate(ingrediente_atualizado.to_dict())

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar ingrediente: {str(e)}"
            )

    @staticmethod
    def remover_ingrediente(ingrediente_id: int) -> bool:
        """Remove um ingrediente pelo ID"""
        ingredienteModel = IngredienteModel()
        try:
            if not IngredienteModel.delete(ingredienteModel):
                raise ValueError("Ingrediente não encontrado ou já removido")
            return True
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao remover ingrediente: {str(e)}"
            )
    @staticmethod
    def get_by_name(nome_ingred: str) -> Optional[Dict[str, Any]]:
        ingrediente = IngredienteModel.get_by_name(nome_ingred)
        return ingrediente.to_dict() if ingrediente else None

    @staticmethod
    def ajustar_estoque(nome_ingrediente: str, quantidade: int) -> IngredienteOut:
        """
        Ajusta a quantidade em estoque de um ingrediente

        Args:
            nome_ingrediente: Nome do ingrediente
            quantidade: Valor a ser adicionado (positivo) ou removido (negativo)

        Returns:
            IngredienteOut: Ingrediente com estoque atualizado
        """
        try:
            if not IngredienteModel.alterar_estoque(nome_ingrediente, quantidade):
                raise ValueError("Falha ao ajustar estoque")

            ingrediente = IngredienteModel.get_by_name(nome_ingrediente)
            return IngredienteOut.model_validate(ingrediente.to_dict())

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao ajustar estoque: {str(e)}"
            )

