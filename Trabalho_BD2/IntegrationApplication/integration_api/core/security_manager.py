import hashlib
import logging
import os
from datetime import datetime, timedelta
from typing import Optional, Dict

from fastapi import HTTPException, Request
from jose import JWTError, jwt, ExpiredSignatureError
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from Trabalho_BD2.IntegrationApplication.integration_api.core.secret_manager import SecretManager
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.user import User
from Trabalho_BD2.IntegrationApplication.integration_api.services.cliente_service import ClienteService
from Trabalho_BD2.IntegrationApplication.integration_api.services.funcionario_service import FuncionarioService

# Configuração detalhada do logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Formato dos logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Handler para console
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)


class SecurityManager:
    def __init__(self):
        logger.info("Inicializando SecurityManager")
        self.secret_manager = SecretManager()
        self.SECRET_KEY = self.secret_manager.get_secret("JWT_SECRET_KEY") or os.getenv("JWT_SECRET_KEY",
                                                                                        "fallback-secret-key")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

        logger.debug("Configurações JWT: ALGORITHM=%s, EXPIRATION=%s min",
                     self.ALGORITHM, self.ACCESS_TOKEN_EXPIRE_MINUTES)

        self.funcionario_service = FuncionarioService()
        self.cliente_service = ClienteService()

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        Autentica um usuário (cliente ou funcionário) com email e senha
        """
        logger.info("Iniciando autenticação para usuário: %s", username)
        try:
            # Log sensível com cuidado (não logar senha real)
            logger.debug("Processando autenticação - username: %s", username)

            senha_hash = hashlib.sha256(password.encode()).hexdigest()
            logger.debug("Hash da senha gerado")

            # Tenta autenticar como cliente
            logger.debug("Tentando autenticação como cliente")
            try:
                cliente = self.cliente_service.obter_cliente_por_email(username)
                if cliente:
                    logger.debug("Cliente encontrado: ID %s", cliente.Id_cliente)

                    # Verifica senha (hash ou texto plano para compatibilidade)
                    if cliente.Senha_cliente == senha_hash or cliente.Senha_cliente == password:
                        logger.info("Autenticação bem-sucedida como cliente: %s", cliente.Id_cliente)
                        return {
                            "username": username,
                            "user_type": "cliente",
                            "user_id": cliente.Id_cliente
                        }
                    else:
                        logger.warning("Senha incorreta para cliente: %s", username)
                else:
                    logger.debug("Nenhum cliente encontrado com email: %s", username)
            except Exception as e:
                logger.error("Erro ao autenticar cliente: %s", str(e), exc_info=True)

            # Tenta autenticar como funcionário
            logger.debug("Tentando autenticação como funcionário")
            try:
                funcionario_id = int(username)
                funcionario = self.funcionario_service.obter_funcionario_por_id(funcionario_id)
                if funcionario:
                    logger.debug("Funcionário encontrado: ID %s", funcionario.Id_func)

                    if funcionario.Senha_Func == senha_hash or funcionario.Senha_Func == password:
                        logger.info("Autenticação bem-sucedida como funcionário: %s", funcionario.Id_func)
                        return {
                            "username": username,
                            "user_type": "funcionario",
                            "user_id": funcionario.Id_func
                        }
                    else:
                        logger.warning("Senha incorreta para funcionário: %s", username)
                else:
                    logger.debug("Nenhum funcionário encontrado com ID: %s", username)
            except ValueError:
                logger.debug("Username não é ID numérico, pulando autenticação de funcionário")
            except Exception as e:
                logger.error("Erro ao autenticar funcionário: %s", str(e), exc_info=True)

            logger.warning("Autenticação falhou para usuário: %s", username)
            return None

        except Exception as e:
            logger.error("Erro inesperado na autenticação: %s", str(e), exc_info=True)
            return None

    def create_access_token(self, user_info: Dict) -> str:
        """
        Cria um token JWT de acesso
        """
        logger.info("Criando token de acesso para: %s", user_info.get("username"))

        if not user_info.get("username") or not user_info.get("user_type"):
            logger.error("Informações do usuário incompletas para criar token")
            raise ValueError("Informações do usuário incompletas para criar token")

        try:
            now = datetime.utcnow()
            expire = now + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

            logger.debug("Token expira em: %s", expire.isoformat())

            to_encode = {
                "sub": user_info["username"],
                "user_type": user_info["user_type"],
                "user_id": user_info.get("user_id"),
                "exp": expire,
                "iat": now
            }

            token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
            logger.debug("Token JWT gerado com sucesso")

            # Log sensível - desativar em produção ou reduzir para DEBUG
            logger.debug("Conteúdo do token: %s", to_encode)

            return token
        except Exception as e:
            logger.error("Erro ao criar token: %s", str(e), exc_info=True)
            raise

    def decode_token(self, token: str) -> Optional[Dict]:
        """
        Decodifica e valida um token JWT
        """
        logger.info("Decodificando token JWT")
        logger.debug("Token recebido: %s", token[:20] + "...")  # Log parcial por segurança

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            # Verifica expiração
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                exp_time = datetime.utcfromtimestamp(exp_timestamp)
                logger.debug("Token válido até: %s", exp_time.isoformat())

                # Verifica se está próximo da expiração
                time_left = (exp_time - datetime.utcnow()).total_seconds() / 60
                if time_left < 5:  # Menos de 5 minutos restantes
                    logger.warning("Token próximo da expiração: %.1f minutos restantes", time_left)

            logger.info("Token decodificado com sucesso para: %s", payload.get("sub"))
            logger.debug("Payload completo: %s", payload)

            return payload
        except ExpiredSignatureError:
            logger.warning("Token expirado")
            return None
        except JWTError as e:
            logger.error("Erro JWT: %s", str(e))
            return None
        except Exception as e:
            logger.error("Erro inesperado ao decodificar token: %s", str(e), exc_info=True)
            return None

    def validate_request(self, request: Request, required_role: str = None) -> User:
        logger.info("Validando requisição para: %s %s", request.method, request.url.path)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            logger.warning("Cabeçalho Authorization ausente")
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Token de autenticação ausente",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not auth_header.startswith("Bearer "):
            logger.warning("Formato inválido do cabeçalho Authorization: %s", auth_header[:20])
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Formato de token inválido",
                headers={"WWW-Authenticate": "Bearer"}
            )

        token = auth_header.split("Bearer ")[1].strip()
        logger.debug("Token extraído: %s...", token[:10])

        payload = self.decode_token(token)

        if not payload:
            logger.warning("Token inválido ou expirado")
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"}
            )

        user_type = payload.get("user_type")
        username = payload.get("sub")

        logger.info("Usuário autenticado: %s (Tipo: %s)", username, user_type)

        if required_role and user_type != required_role:
            logger.warning(
                "Acesso negado: usuário %s (%s) tentou acessar recurso que requer %s",
                username, user_type, required_role
            )
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Acesso não autorizado para este tipo de usuário"
            )

        # Adaptar payload para o schema User
        user_data = {
            "username": username,
            "user_type": user_type,
            "user_id": payload.get("user_id")
        }

        logger.debug("Retornando objeto User: %s", user_data)
        return User(**user_data)

    # Dependências para uso no FastAPI
    def get_current_user(self, request: Request) -> User:
        logger.debug("Dependência get_current_user iniciada")
        return self.validate_request(request)

    def get_current_funcionario(self, request: Request) -> User:
        logger.debug("Dependência get_current_funcionario iniciada")
        return self.validate_request(request, required_role="funcionario")

    def get_current_cliente(self, request: Request) -> User:
        logger.debug("Dependência get_current_cliente iniciada")
        return self.validate_request(request, required_role="cliente")