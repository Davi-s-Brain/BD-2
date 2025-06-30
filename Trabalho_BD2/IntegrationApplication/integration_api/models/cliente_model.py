from __future__ import annotations

import hashlib
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Any

from fastapi import HTTPException

from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection
from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.cliente_schemas import ClienteCreate, ClienteUpdate, \
    ClienteOut


class ClienteModel:
    def __init__(self, db_access: DatabaseAccess = None):
        self.logger = logging.getLogger('ClienteModel')
        self.db = db_access or DatabaseAccess(get_connection)
        self.logger.setLevel(logging.DEBUG)

    def criar_cliente(self, cliente_data: ClienteCreate) -> ClienteOut:
        # Gera ID somente se a tabela não for auto-increment
        id_cliente = self._gerar_id_cliente()
        print(f"O id do cliente eh {cliente_data.Id_cliente}")
        cliente_dict = {
            'Id_cliente': id_cliente,
            'Primeiro_nome_client': str(cliente_data.Primeiro_nome_client),
            'Ultimo_nome_client': str(cliente_data.Ultimo_nome_client),
            'Data_nascimento_client': cliente_data.Data_nascimento_client.isoformat(),
            'CPF_client': int(cliente_data.CPF_client),
            'Telefone_client': int(cliente_data.Telefone_client),
            'E_mail_client': str(cliente_data.E_mail_client),
            'Genero_client': str(cliente_data.Genero_client),
            'Senha_cliente': hashlib.sha256(cliente_data.Senha_cliente.encode()).hexdigest(),
            'Data_cadastro_client': datetime.now().date().isoformat(),
            'E_intolerante_lactose': 1 if cliente_data.E_intolerante_lactose else 0,
            'E_celiaco': 1 if cliente_data.E_celiaco else 0,
            'E_vegetariano': 1 if cliente_data.E_vegetariano else 0,
            'E_vegano': 1 if cliente_data.E_vegano else 0
        }

        # Adiciona ID somente se foi gerado
        if id_cliente is not None:
            cliente_dict['Id_cliente'] = id_cliente

        try:
            inserted_id = self.db.add("Cliente", cliente_dict)

            # Busca usando o ID retornado pelo banco
            cliente = self.buscar_por_id(inserted_id)
            if not cliente:
                # Tenta buscar por CPF como fallback
                cliente = self._buscar_cliente_por_cpf(cliente_data.CPF_client)
                if not cliente:
                    raise ValueError("Cliente não encontrado após inserção")

            return cliente

        except Exception as e:
            self.logger.error(f"Erro ao criar cliente: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Falha ao criar cliente: {str(e)}"
            )

    def _gerar_id_cliente(self) -> int:
        resultado = self.db._execute_query("SELECT MAX(Id_cliente) AS max_id FROM Cliente", fetch=True)
        max_id_str = resultado[0]['max_id'] if resultado and resultado[0]['max_id'] is not None else 0
        return int(max_id_str) + 1

    def _buscar_cliente_por_cpf(self, cpf: int) -> Optional[ClienteOut]:
        """Busca alternativa por CPF caso a busca por ID falhe"""
        result = self.db.get_one("Cliente", conditions={"CPF_client": cpf})
        if result:
            return self._row_to_cliente_out(result)
        return None

    def buscar_por_id(self, Id_cliente: int) -> Optional[ClienteOut]:
        try:
            # Tenta converter para int (caso seja string)
            id_int = int(Id_cliente)
            row = self.db.get_one("Cliente", conditions={"Id_cliente": id_int})

            if not row:
                return None

            return self._row_to_cliente_out(row)

        except (ValueError, TypeError) as e:
            print(f"ID inválido: {Id_cliente} - {str(e)}")
            return None

    def buscar_por_email(self, E_mail_client: str) -> Optional[ClienteOut]:
        """
        Busca um cliente pelo email

        Args:
            E_mail_client: Email do cliente

        Returns:
            ClienteOut se encontrado, None caso contrário
        """
        row = self.db.get_one("Cliente", conditions={"E_mail_client": E_mail_client})
        if not row:
            return None
        return self._row_to_cliente_out(row)

    def buscar_por_cpf(self, CPF_client: int) -> Optional[ClienteOut]:
        """
        Busca um cliente pelo CPF

        Args:
            CPF_client: CPF do cliente

        Returns:
            ClienteOut se encontrado, None caso contrário
        """
        row = self.db.get_one("Cliente", conditions={"CPF_client": CPF_client})
        print(row)
        if not row:
            return None
        return self._row_to_cliente_out(row)

    def listar_clientes(self) -> List[ClienteOut]:
        """
        Lista todos os clientes cadastrados

        Returns:
            Lista de ClienteOut
        """
        rows = self.db.get("Cliente")
        return [self._row_to_cliente_out(row) for row in rows]

    def atualizar_cliente(self, Id_cliente: int, update_data: ClienteUpdate) -> Optional[ClienteOut]:
        """
        Atualiza os dados de um cliente

        Args:
            Id_cliente: ID do cliente a ser atualizado
            update_data: Dados parciais para atualização

        Returns:
            ClienteOut atualizado se encontrado, None caso contrário
        """
        # Remove campos não informados
        update_dict = update_data.model_dump(exclude_unset=True, exclude={'Id_cliente'})

        if not update_dict:
            return self.buscar_por_id(Id_cliente)

        # Se houver senha, faz hash
        if 'Senha_cliente' in update_dict:
            update_dict['Senha_cliente'] = hashlib.sha256(update_dict['Senha_cliente'].encode()).hexdigest()

        # Converte datas para string ISO se presentes
        if 'Data_nascimento_client' in update_dict:
            update_dict['Data_nascimento_client'] = update_dict['Data_nascimento_client'].isoformat()

        # Executa a atualização
        self.db.update("Cliente", update_dict, {"Id_cliente": Id_cliente})

        # Retorna o cliente atualizado
        return self.buscar_por_id(Id_cliente)

    def remover_cliente(self, Id_cliente: int) -> bool:
        """
        Remove um cliente do banco de dados

        Args:
            Id_cliente: ID do cliente a ser removido

        Returns:
            True se removido com sucesso, False caso contrário
        """
        # Verifica se existe antes de deletar
        if not self.buscar_por_id(Id_cliente):
            return False

        self.db.delete("Cliente", {"Id_cliente": Id_cliente})
        return True

    def _row_to_cliente_out(self, row: dict) -> ClienteOut:
        """
        Converte uma linha do banco para o schema ClienteOut

        Args:
            row: Dicionário com dados do cliente

        Returns:
            ClienteOut: Cliente convertido
        """
        # Converte booleanos (SQLite armazena como 0/1)
        bool_fields = [
            'E_intolerante_lactose',
            'E_celiaco',
            'E_vegetariano',
            'E_vegano'
        ]

        for field in bool_fields:
            if field in row:
                row[field] = bool(row[field])

        # Converte datas
        if 'Data_nascimento_client' in row and row['Data_nascimento_client']:
            row['Data_nascimento_client'] = datetime.fromisoformat(row['Data_nascimento_client'])

        if 'Data_cadastro_client' in row and row['Data_cadastro_client']:
            row['Data_cadastro_client'] = datetime.fromisoformat(row['Data_cadastro_client'])

        return ClienteOut(**row)