from typing import List, Optional

from fastapi import HTTPException, status

from Trabalho_BD2.IntegrationApplication.integration_api.models.func_model import FuncionarioModel
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.funcionario import (
    FuncionarioCreate,
    FuncionarioUpdate,
    FuncionarioOut
)


class FuncionarioService:
    def __init__(self, funcionario_model: FuncionarioModel = None):
        """Inicializa o serviço com a model injetada"""
        self.model = funcionario_model or FuncionarioModel()

    def create(self, funcionario_data: FuncionarioCreate) -> FuncionarioOut:
        """
        Cria um novo funcionário no sistema

        Args:
            funcionario_data: Dados do funcionário a ser criado

        Returns:
            FuncionarioOut: Funcionário criado com todos os dados
        """
        return self.model.create(funcionario_data)

    def get_all(self) -> List[FuncionarioOut]:
        """
        Retorna todos os funcionários cadastrados

        Returns:
            List[FuncionarioOut]: Lista de funcionários
        """
        return self.model.get_all()

    def get_by_id(self, func_id: int) -> Optional[FuncionarioOut]:
        """
        Busca um funcionário pelo ID

        Args:
            func_id: ID do funcionário

        Returns:
            FuncionarioOut se encontrado, None caso contrário
        """
        return self.model.get_by_id(func_id)

    def update(self, func_id: int, update_data: FuncionarioUpdate) -> Optional[FuncionarioOut]:
        """
        Atualiza os dados de um funcionário

        Args:
            func_id: ID do funcionário a ser atualizado
            update_data: Dados parciais para atualização

        Returns:
            FuncionarioOut atualizado se encontrado, None caso contrário
        """
        return self.model.update(func_id, update_data)

    def delete(self, func_id: int) -> bool:
        """
        Remove um funcionário do sistema

        Args:
            func_id: ID do funcionário a ser removido

        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        return self.model.delete(func_id)

    def update_senha_funcionario(self, func_id: int, nova_senha: str) -> Optional[FuncionarioOut]:
        """
        Atualiza a senha de um funcionário

        Args:
            func_id: ID do funcionário
            nova_senha: Nova senha

        Returns:
            FuncionarioOut atualizado se encontrado, None caso contrário
        """
        return self.model.update_password(func_id, nova_senha)

    def obter_funcionario_por_email(self, email: str) -> FuncionarioOut:
        """
        Obtém um funcionário pelo email

        Args:
            email: Email do funcionário

        Returns:
            FuncionarioOut: Funcionário encontrado

        Raises:
            HTTPException: Se funcionário não for encontrado
        """
        funcionario = self.model.buscar_por_email(email)
        if not funcionario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Funcionário não encontrado"
            )
        return funcionario
    def obter_funcionario_por_id(self, id: int) -> FuncionarioOut:
        """
        Obtém um funcionário pelo email

        Args:
            email: Email do funcionário

        Returns:
            FuncionarioOut: Funcionário encontrado

        Raises:
            HTTPException: Se funcionário não for encontrado
        """
        funcionario = self.model.get_by_id(id)
        if not funcionario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Funcionário não encontrado"
            )
        return funcionario