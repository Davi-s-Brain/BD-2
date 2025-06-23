import hashlib
import logging
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import Request, HTTPException
from jose import JWTError, jwt, ExpiredSignatureError
from starlette.status import HTTP_401_UNAUTHORIZED

from Trabalho_BD2.IntegrationApplication.integration_api.core.secret_manager import SecretManager
from Trabalho_BD2.IntegrationApplication.integration_api.services.funcionario_service import FuncionarioService


class SecurityManager:
    def __init__(self):
        self.secret_manager = SecretManager()
        self.SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

        # Inicializa o banco de dados
        self._users_db = sqlite3.connect('local.db', check_same_thread=False)
        self._users_db.row_factory = sqlite3.Row

        # Cria a tabela se não existir
        with self._users_db as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users 
                (username TEXT PRIMARY KEY, password TEXT, id INTEGER)''')
            conn.execute('''INSERT OR IGNORE INTO users (username, password, id) 
                VALUES ('admin', 'admin', 1)''')

    def create_user(self, username: str, password: str):
        try:
            with self._users_db as conn:
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                return {"username": username, "password": password}
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None

    import hashlib

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        try:
            self._users_db.row_factory = sqlite3.Row
            cursor = self._users_db.cursor()

            cursor.execute(
                "SELECT E_mail_client, Senha_cliente FROM Cliente WHERE E_mail_client = ?",
                (username,)
            )

            user = cursor.fetchone()

            if user:
                senha_hash = hashlib.sha256(password.encode()).hexdigest()
                print("Hash digitado:", senha_hash)
                print("Hash do banco:", user["Senha_cliente"])

                if user["Senha_cliente"] == senha_hash:
                    return {"username": user["E_mail_client"]}
            return None
        except Exception as e:
            print(f"Erro na autenticação: {e}")
            return None

    def get_current_user(self, token: str) -> Dict:
        """Get current user from token"""
        print(token)
        payload = self.decode_token(token)
        print(payload)
        if not payload:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        username = payload.get("sub")
        cursor = self._users_db.cursor()
        cursor.execute(
            "SELECT username, password FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()

        if not user:
            functionService = FuncionarioService()
            funcionario = functionService.get_by_id(username)
            if funcionario:
                return {"username": str(funcionario.Id_func), "password": funcionario.Senha_func}
            if not user:
                raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {"username": user['username'], "password": user['password']}

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        now = datetime.utcnow()
        expire = now + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),  # <- ajuda a garantir diferença
        })

        jwtencode = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        print("O token gerado foi "+jwtencode)
        return jwtencode


    def decode_token(self, token: str) -> Optional[Dict]:
        try:
            # Decodifica o token usando a chave e algoritmo
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            # Verifica se o campo 'sub' existe
            subject = payload.get("sub")
            if subject is None:
                print("⚠️ Token inválido: campo 'sub' ausente.")
                return None

            # Se quiser logar o payload para debug
            print(f"✅ Token decodificado com sucesso: {payload}")

            # Verificação extra: opcional
            exp = payload.get("exp")
            if exp:
                exp_datetime = datetime.fromtimestamp(exp)
                print(f"🔒 Token expira em: {exp_datetime}")

            return payload

        except ExpiredSignatureError:
            print("⛔ Token expirado.")
            return None
        except JWTError as e:
            print(f"⛔ Erro ao decodificar token JWT: {e}")
            return None
        except Exception as e:
            print(f"⛔ Erro inesperado: {e}")

    def validate(self, request: Request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        token = token.removeprefix("Bearer ").strip()

        # Validação do token JWT
        payload = self.decode_token(token)
        if payload:
            username = payload.get("sub")
            cursor = self._users_db.cursor()
            cursor.execute(
                "SELECT username FROM users WHERE username = ?",
                (username,)
            )
            if cursor.fetchone():
                return username

        # Validação da API key
        expected_key = self.secret_manager.get_secret("API_KEY")
        if token == expected_key:
            return "api_key_user"

        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    def __del__(self):
        if hasattr(self, '_users_db'):
            self._users_db.close()