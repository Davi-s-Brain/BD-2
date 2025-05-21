import logging
import os
from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import Request, HTTPException
from jose import JWTError, jwt
from starlette.status import HTTP_401_UNAUTHORIZED
from Trabalho_BD2.IntegrationApplication.integration_api.core.secret_manager import SecretManager

class SecurityManager:
    def __init__(self):
        self.secret_manager = SecretManager()
        self.SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")  # Change in production
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        # Mock user database - Replace with real database in production
        self._users_db = {
            "admin": {
                "username": "admin",
                "password": "admin"  # Using API_KEY as admin password
            }
        }

        self._func_db = {
            "admin": {
                "username": "admin",
                "password": self.secret_manager.get_secret("API_KEY")  # Using API_KEY as admin password
            }
        }

    def create_user(self, username: str, password: str):
        try:

            novo_usuario = {
                "username": username,
                "password": password
            }
            self._users_db[username] = novo_usuario

            return novo_usuario
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        user = self._users_db.get(username)
        if user and user["password"] == password:
            return user
        return None
    def create_func(self, username: str, password: str):
        try:

            novo_usuario = {
                "username": username,
                "password": password
            }
            self._func_db[username] = novo_usuario

            return novo_usuario
        except Exception as e:
            print(f"Erro ao criar funcionário: {e}")
            return None
    def authenticate_func(self, username: str, password: str) -> Optional[Dict]:
        user = self._func_db.get(username)
        if user and user["password"] == password:
            return user
        return None

    def create_access_token(self, data: dict) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def decode_token(self, token: str) -> Optional[Dict]:
        """Decode and validate a JWT token"""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except JWTError:
            return None

    def validate(self, request: Request):
        """Validate both JWT tokens and API keys"""
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        token = token.removeprefix("Bearer ").strip()

        # First try JWT token validation
        payload = self.decode_token(token)
        if payload:
            username = payload.get("sub")
            if username and username in self._users_db:
                return username

        # If JWT validation fails, try API key validation
        expected_key = self.secret_manager.get_secret("API_KEY")
        if token == expected_key:
            return "api_key_user"

        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    def get_current_user(self, token: str) -> Dict:
        """Get current user from token"""
        payload = self.decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        username = payload.get("sub")
        user = self._users_db.get(username)

        if not user:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    def update(self, user_data):

     pass