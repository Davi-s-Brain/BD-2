from __future__ import annotations

from typing import Optional, List

from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.funcionario import FuncionarioCreate, \
    FuncionarioUpdate, FuncionarioOut
from ..db.database_acess import DatabaseAccess


class FuncionarioModel:
    def __init__(self, db_access: DatabaseAccess = None):
        self.db = db_access or DatabaseAccess(get_connection)

    def create(self, funcionario: FuncionarioCreate) -> FuncionarioOut:
        """
        Cria um novo funcionário no banco de dados

        Args:
            funcionario: Dados do funcionário a ser criado

        Returns:
            FuncionarioOut: Funcionário criado com ID gerado
        """
        # Remove Id_func pois será gerado pelo banco
        funcionario_data = funcionario.model_dump()

        # Converte datas para string
        funcionario_data['Data_nasc_func'] = funcionario_data['Data_nasc_func'].isoformat()
        funcionario_data['Data_admissao'] = funcionario_data['Data_admissao'].isoformat()

        # Insere no banco
        id_func = funcionario_data['Id_func']

        # Retorna o funcionário criado
        return self.get_by_id(id_func)

    def get_by_id(self, id_func: int) -> Optional[FuncionarioOut]:
        """
        Busca um funcionário pelo ID

        Args:
            id_func: ID do funcionário a ser buscado

        Returns:
            FuncionarioOut se encontrado, None caso contrário
        """
        row = self.db.get_one("funcionario", conditions={"Id_func": id_func})
        if not row:
            return None

        # Converte para schema de saída
        return FuncionarioOut(**row)

    def get_all(self) -> List[FuncionarioOut]:
        """
        Retorna todos os funcionários cadastrados

        Returns:
            Lista de FuncionarioOut
        """
        rows = self.db.get("funcionario")
        return [FuncionarioOut(**row) for row in rows]

    def update(self, id_func: int, funcionario_update: FuncionarioUpdate) -> Optional[FuncionarioOut]:
        """
        Atualiza os dados de um funcionário

        Args:
            id_func: ID do funcionário a ser atualizado
            funcionario_update: Dados a serem atualizados

        Returns:
            FuncionarioOut atualizado ou None se não encontrado
        """
        # Remove campos não informados (None)
        update_data = funcionario_update.model_dump(exclude_unset=True, exclude={'Id_func'})

        if not update_data:
            return self.get_by_id(id_func)

        # Converte datas para string se presentes
        if 'Data_nasc_func' in update_data:
            update_data['Data_nasc_func'] = update_data['Data_nasc_func'].isoformat()
        if 'Data_admissao' in update_data:
            update_data['Data_admissao'] = update_data['Data_admissao'].isoformat()

        # Executa a atualização
        self.db.update("funcionario", update_data, {"Id_func": id_func})

        # Retorna o funcionário atualizado
        return self.get_by_id(id_func)

    def delete(self, id_func: int) -> bool:
        """
        Remove um funcionário do banco de dados

        Args:
            id_func: ID do funcionário a ser removido

        Returns:
            True se removido com sucesso, False caso contrário
        """
        # Verifica se existe antes de deletar
        if not self.get_by_id(id_func):
            return False

        self.db.delete("funcionario", {"Id_func": id_func})
        return True

    def update_password(self, id_func: int, new_password: str) -> Optional[FuncionarioOut]:
        """
        Atualiza a senha de um funcionário

        Args:
            id_func: ID do funcionário
            new_password: Nova senha

        Returns:
            FuncionarioOut atualizado ou None se não encontrado
        """
        self.db.update(
            "funcionario",
            {"Senha_func": new_password},
            {"Id_func": id_func}
        )
        return self.get_by_id(id_func)

    def buscar_por_email(self, email: str) -> Optional[FuncionarioOut]:
        """
        Busca um funcionário pelo email

        Args:
            email: Email do funcionário

        Returns:
            FuncionarioOut se encontrado, None caso contrário
        """
        return self.db.get_one(
            "funcionario",
            conditions={"E_mail_func": email}
        )