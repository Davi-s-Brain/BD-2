from __future__ import annotations
from typing import Dict, Optional
from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection
from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess
import hashlib
import logging

logger = logging.getLogger(__name__)


class UserModel:
    def __init__(self, db_access: DatabaseAccess = None):
        self.db = db_access or DatabaseAccess(get_connection)
        self.user_fields = ["username", "password", "id"]  # Campos esperados

    def _convert_row(self, row) -> dict:
        """Converte tupla para dicionário usando os campos do schema"""
        if isinstance(row, dict):
            return row
        return dict(zip(self.user_fields, row))

    def create_user(self, username: str, password: str) -> Optional[Dict]:
        """
        Cria um novo usuário no banco de dados

        Args:
            username: Nome de usuário
            password: Senha em texto claro

        Returns:
            Dicionário com dados do usuário ou None em caso de erro
        """
        try:
            # Criptografa a senha antes de armazenar
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            user_data = {
                'username': username,
                'password': hashed_password
            }

            user_id = self.db.add("users", user_data)
            if not user_id:
                logger.error("Falha ao criar usuário: ID não retornado")
                return None

            return self.get_user_by_username(username)
        except Exception as e:
            logger.error(f"Erro ao criar usuário {username}: {str(e)}")
            return None

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Busca um usuário pelo nome de usuário

        Args:
            username: Nome de usuário

        Returns:
            Dicionário com dados do usuário ou None se não encontrado
        """
        try:
            row = self.db.get_one(
                "users",
                conditions={"username": username}
            )
            return self._convert_row(row) if row else None
        except Exception as e:
            logger.error(f"Erro ao buscar usuário {username}: {str(e)}")
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        Autentica um usuário com base nas credenciais

        Args:
            username: Nome de usuário
            password: Senha em texto claro

        Returns:
            Dicionário com dados do usuário se autenticação for válida
        """
        try:
            user = self.get_user_by_username(username)
            if not user:
                logger.warning(f"Usuário não encontrado: {username}")
                return None

            hashed_input = hashlib.sha256(password.encode()).hexdigest()

            if user['password'] == hashed_input:
                return user

            logger.warning(f"Senha inválida para usuário {username}")
            return None
        except Exception as e:
            logger.error(f"Erro na autenticação de {username}: {str(e)}")
            return None