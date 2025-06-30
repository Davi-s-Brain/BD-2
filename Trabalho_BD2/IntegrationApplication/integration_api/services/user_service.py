from __future__ import annotations
from typing import Dict, Optional
from fastapi import HTTPException, status
from Trabalho_BD2.IntegrationApplication.integration_api.models.user_model import UserModel
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.user import (
    UserCreate,
    UserOut,
    UserLogin,
    UserUpdate
)
import logging

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_model: UserModel = None):
        self.model = user_model or UserModel()

    def create_user(self, user_data: UserCreate) -> UserOut:
        """
        Cria um novo usuário no sistema

        Args:
            user_data: Dados do usuário a ser criado

        Returns:
            UserOut: Dados do usuário criado

        Raises:
            HTTPException: Em caso de erro na criação
        """
        try:
            # Verifica se usuário já existe
            if self.model.get_user_by_username(user_data.username):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already registered"
                )

            # Cria o usuário
            created_user = self.model.create_user(
                username=user_data.username,
                password=user_data.password
            )

            if not created_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user"
                )

            return UserOut(
                username=created_user['username'],
                id=created_user['id']
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def authenticate(self, credentials: UserLogin) -> Dict:
        """
        Autentica um usuário com base nas credenciais

        Args:
            credentials: Dados de login

        Returns:
            Dict: Dados do usuário autenticado

        Raises:
            HTTPException: Em caso de autenticação falha
        """
        try:
            user = self.model.authenticate_user(
                username=credentials.username,
                password=credentials.password
            )

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return user

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_user(self, username: str) -> Optional[UserOut]:
        """
        Obtém os dados de um usuário pelo username

        Args:
            username: Nome de usuário para busca

        Returns:
            UserOut se encontrado, None caso contrário
        """
        try:
            user_data = self.model.get_user_by_username(username)
            if not user_data:
                return None

            return UserOut(
                username=user_data['username'],
                id=user_data['id']
            )
        except Exception as e:
            logger.error(f"Error getting user {username}: {str(e)}")
            return None

    def update_user(self, username: str, update_data: UserUpdate) -> UserOut:
        """
        Atualiza os dados de um usuário

        Args:
            username: Nome de usuário a ser atualizado
            update_data: Dados para atualização

        Returns:
            UserOut: Dados atualizados do usuário

        Raises:
            HTTPException: Em caso de erro na atualização
        """
        try:
            # Verifica se usuário existe
            current_user = self.model.get_user_by_username(username)
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Atualiza apenas a senha se fornecida
            if update_data.password:
                updated_user = self.model.create_user(
                    username=username,
                    password=update_data.password
                )
            else:
                updated_user = current_user

            if not updated_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update user"
                )

            return UserOut(
                username=updated_user['username'],
                id=updated_user['id']
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating user {username}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def delete_user(self, username: str) -> bool:
        """
        Remove um usuário do sistema

        Args:
            username: Nome de usuário a ser removido

        Returns:
            bool: True se removido com sucesso

        Raises:
            HTTPException: Em caso de erro na remoção
        """
        try:
            # Verifica se usuário existe
            if not self.model.get_user_by_username(username):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # TODO: Implementar método delete no UserModel
            # return self.model.delete_user(username)
            raise NotImplementedError("Delete method not implemented in UserModel")

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting user {username}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )