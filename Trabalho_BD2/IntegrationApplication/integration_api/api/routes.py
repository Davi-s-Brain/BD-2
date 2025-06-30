import sqlite3
from datetime import date
from typing import List, Dict, Any, Annotated

from fastapi import APIRouter, Request, Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from Trabalho_BD2.IntegrationApplication.integration_api.core.limiter import limiter
from Trabalho_BD2.IntegrationApplication.integration_api.core.security_manager import SecurityManager
from Trabalho_BD2.IntegrationApplication.integration_api.core.totalizador import totalizador_diario
from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess
from Trabalho_BD2.IntegrationApplication.integration_api.models.combo_model import ComboModel
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.carrinho_schemas import (
    ItemCarrinhoSchema,
    CarrinhoOutSchema,
    CarrinhoUpdateSchema, ContagemCategoriasOutSchema
)
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.cliente_schemas import (
    ClienteCreate,
    ClienteUpdate,
    ClienteOut
)
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.funcionario import (
    FuncionarioCreate,
    FuncionarioUpdate,
    FuncionarioOut,
)
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.generics import ComboDisponibilidadeResponse, \
    ComboDisponibilidadeRequest
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.ingrediente_schemas import IngredienteOut, \
    IngredienteCreate, IngredienteUpdate
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.item import ItemCreate, ItemUpdate, ItemDelete
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.order import CreateOrder
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoOut
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.user import UserLogin, Token, User, UserCreate, UserOut
from Trabalho_BD2.IntegrationApplication.integration_api.services.carrinho_service import CarrinhoService
from Trabalho_BD2.IntegrationApplication.integration_api.services.cliente_service import ClienteService
from Trabalho_BD2.IntegrationApplication.integration_api.services.funcionario_service import FuncionarioService
from Trabalho_BD2.IntegrationApplication.integration_api.services.ingrediente_service import IngredienteService
from Trabalho_BD2.IntegrationApplication.integration_api.services.item_service import ItemService
from Trabalho_BD2.IntegrationApplication.integration_api.services.pedido import PedidoService
from Trabalho_BD2.IntegrationApplication.integration_api.services.user_service import UserService

service = ItemService()
security = SecurityManager()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Routers
router = APIRouter(prefix="/integration", tags=["Integration"])
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
func_router = APIRouter(
    prefix="/funcionarios",
    tags=["Funcionario"],
)

funcService = FuncionarioService()
# Router para Ingredientes
ingrediente_router = APIRouter(
    prefix="/ingredientes",
    tags=["Ingrediente"],
)



ingredienteService = IngredienteService()
# Configuração do router
cliente_router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
)

cliente_service = ClienteService()

import logging

logger = logging.getLogger(__name__)
combo_router = APIRouter(prefix="/combos", tags=["Combos"])


@combo_router.post(
    "/verificar-disponibilidade",
    response_model=ComboDisponibilidadeResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("10/minute")
async def verificar_disponibilidade_combo(
        request: Request,
        combo_data: ComboDisponibilidadeRequest):
    """
    Verifica a disponibilidade de um combo de produtos no estoque.

    Parâmetros:
    - id_lanche: ID do lanche (opcional)
    - id_bebida: ID da bebida (opcional)
    - id_sobremesa: ID da sobremesa (opcional)
    - id_acompanhamento: ID do acompanhamento (opcional)

    Retorna:
    - Lista de itens com suas quantidades em estoque
    - Mensagem de status geral
    - Flag indicando se o combo está totalmente disponível
    - Timestamp da verificação
    """
    try:
        combo_model = ComboModel()
        resultados = combo_model.verificar_disponibilidade(
            id_lanche=combo_data.id_lanche,
            id_bebida=combo_data.id_bebida,
            id_sobremesa=combo_data.id_sobremesa,
            id_acompanhamento=combo_data.id_acompanhamento
        )

        disponivel = all(item.quantidade_estoque > 0 for item in resultados)
        status_geral = "Combo disponível" if disponivel else "Alguns itens estão indisponíveis"

        return {
            "itens": resultados,
            "status_geral": status_geral,
            "disponivel": disponivel
        }

    except Exception as e:
        logger.error(f"Erro ao verificar disponibilidade: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar disponibilidade do combo: {str(e)}"
        )
@limiter.limit("5/minute")
@cliente_router.post(
    "/clientes",
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo cliente", response_model = Token)  # Use o schema Pydantic aqui

async def criar_cliente(request: Request, cliente_data: ClienteCreate):
    """
    Cria um novo cliente

    - **Nome_cliente**: Nome completo do cliente
    - **E_mail_client**: E-mail único do cliente
    - **Telefone_client**: Telefone para contato
    - **Senha_cliente**: Senha (será hasheada)
    """
    cliente_service.criar_cliente(cliente_data)
    try:
        # Autentica usando SecurityManager que verifica clientes e funcionários
        user_info = security.authenticate_user(str(cliente_data.E_mail_client), cliente_data.Senha_cliente)
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Gera token com informações do usuário
        access_token = security.create_access_token(user_info)
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno durante autenticação"
        )

@cliente_router.get(
    "/",
    response_model=List[ClienteOut]
)
@limiter.limit("10/minute")
async def listar_clientes(request: Request):
    """Lista todos os clientes"""
    return cliente_service.listar_clientes()


@cliente_router.get(
    "/{cliente_id}",
    response_model=ClienteOut
)
@limiter.limit("10/minute")
async def obter_cliente(
        request: Request,
        cliente_id: Annotated[int, Path(..., description="ID do cliente")]
):
    """Obtém um cliente específico pelo ID"""
    cliente = cliente_service.obter_cliente(cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return cliente

@auth_router.get(
    "/email/{email}",
    response_model=ClienteOut
)
@limiter.limit("10/minute")
async def obter_cliente(
        request: Request,
        email: Annotated[str, Path(..., description="Email do cliente")]
):
    """Obtém um cliente específico pelo email"""
    cliente = cliente_service.obter_cliente_por_email(email)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return cliente


@cliente_router.put(
    "/{cliente_id}",
    response_model=ClienteOut
)
@limiter.limit("5/minute")
async def atualizar_cliente(
        request: Request,
        cliente_id: Annotated[int, Path(..., description="ID do cliente")],
        cliente_data: ClienteUpdate,
        current_user: User = Depends(security.get_current_user)
):
    """Atualiza um cliente existente"""
    try:
        # Verifica se o usuário está atualizando seu próprio perfil
        if current_user['Id_cliente'] != cliente_id and not current_user.get('is_admin', False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você só pode atualizar seu próprio perfil"
            )

        atualizado = cliente_service.atualizar_cliente(cliente_id, cliente_data)
        if not atualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
        return cliente_service.obter_cliente(cliente_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@cliente_router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@limiter.limit("5/minute")
async def remover_cliente(
        request: Request,
        cliente_id: Annotated[int, Path(..., description="ID do cliente")],
        current_user: User = Depends(security.get_current_user)
):
    """Remove um cliente"""
    try:
        # Verifica se o usuário é admin ou está removendo seu próprio perfil
        if current_user['Id_cliente'] != cliente_id and not current_user.get('is_admin', False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para remover este cliente"
            )

        removido = cliente_service.remover_cliente(cliente_id)
        if not removido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@cliente_router.get(
    "/me",
    response_model=ClienteOut
)
@limiter.limit("10/minute")
async def obter_meu_perfil(
        request: Request,
        current_user: User = Depends(security.get_current_user)
):
    """Obtém o perfil do cliente logado"""
    cliente = cliente_service.obter_cliente(current_user['Id_cliente'])
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return cliente
@ingrediente_router.post(
    "/",
    response_model=IngredienteOut,
    status_code=status.HTTP_201_CREATED
)

async def create_ingrediente(data: IngredienteCreate):
    """Cria um novo ingrediente"""
    new_id = ingredienteService.create(data)
    return ingredienteService.obter_por_id(new_id.Id_ingred)

@ingrediente_router.get(
    "/",
    response_model= List[IngredienteOut]
)
async def list_ingredientes():
    """Lista todos os ingredientes"""
    return ingredienteService.obter_todos()

@ingrediente_router.get(
    "/{ingrediente_id}",
    response_model=IngredienteOut
)
async def get_ingrediente(ingrediente_id: int):
    """Obtém um ingrediente específico pelo ID"""
    ingrediente = ingredienteService.obter_por_id(ingrediente_id)
    if not ingrediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não encontrado"
        )
    return ingrediente

@ingrediente_router.put(
    "/{ingrediente_id}",
    response_model=Dict[str, Any]
)
async def update_ingrediente(
    ingrediente_id: int,
    data: IngredienteUpdate
):
    """Atualiza um ingrediente existente"""
    atualizado = ingredienteService.atualizar_ingrediente(ingrediente_id, data)
    if not atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não encontrado"
        )
    return ingredienteService.obter_por_id(ingrediente_id)

@ingrediente_router.delete(
    "/{ingrediente_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_ingrediente(ingrediente_id: int):
    """Remove um ingrediente"""
    deleted = ingredienteService.remover_ingrediente(ingrediente_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não encontrado"
        )

@func_router.post(
    "/",
    response_model=FuncionarioOut,
    status_code=status.HTTP_201_CREATED
)
async def create_funcionario(data: FuncionarioCreate):
    return funcService.create(data)

@func_router.get(
    "/",
    response_model=List[FuncionarioOut]
)
async def list_funcionarios():
    return funcService.get_all()

@func_router.get(
    "/{func_id}",
    response_model=FuncionarioOut
)
async def get_funcionario(func_id: int):
    func = funcService.get_by_id(func_id)
    if not func:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    return func

@func_router.put(
    "/{func_id}",
    response_model=FuncionarioOut
)
async def update_funcionario(
    func_id: int,
    data: FuncionarioUpdate
):
    updated = funcService.update(func_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    return funcService.get_by_id(func_id)

@func_router.delete(
    "/{func_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_funcionario(func_id: int):
    deleted = funcService.delete(func_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> User:
    payload = security.get_current_user(request)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return security.get_current_user(request)


def get_db_access() -> DatabaseAccess:
    """Factory que retorna uma instância de DatabaseAccess"""

    def get_connection():
        conn = sqlite3.connect('data.sqlite')
        # Configurações adicionais para SQLite
        conn.row_factory = sqlite3.Row
        return conn

    return DatabaseAccess(get_connection)  # Retorna INSTÂNCIA de DatabaseAccess


router_carrinho = APIRouter(prefix="/carrinho", tags=["Carrinho"])

# Cria a instância CORRETA
db_access_instance = get_db_access()

# Passa para o serviço
service_carrinho = CarrinhoService(db_access=db_access_instance)

@router_carrinho.get("/", response_model=CarrinhoOutSchema)
async def obter_carrinho(current_user: User = Depends(get_current_user)):
    """
    Obtém o carrinho do usuário atual
    """
    print(current_user.username)
    try:
        cliente = cliente_service.obter_cliente_por_email(current_user.username)
        print(current_user.username)
        print(cliente.Id_cliente)
        carrinho = service_carrinho.obter_carrinho(cliente.Id_cliente)

        if not carrinho or not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrinho ou cliente não encontrados"
            )
        return carrinho
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router_carrinho.post("/item", response_model=CarrinhoOutSchema)
async def adicionar_item(
    item: ItemCarrinhoSchema,
    current_user: User = Depends(get_current_user)
):
    """
    Adiciona um item ao carrinho
    """
    cliente = cliente_service.obter_cliente_por_email(current_user.username)
    try:

        return service_carrinho.adicionar_item(cliente.Id_cliente, item.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router_carrinho.get(
    "/contagem-categorias",
    response_model=ContagemCategoriasOutSchema,
    summary="Obtém a contagem de itens por categoria no carrinho",
    description="Retorna um JSON com as categorias e a quantidade de itens em cada uma"
)
async def obter_contagem_categorias(
        current_user: User = Depends(get_current_user)
):
    """
    Obtém a contagem de itens agrupados por categoria no carrinho do usuário atual
    """
    try:
        cliente = cliente_service.obter_cliente_por_email(current_user.username)
        contagem = service_carrinho.contar_itens_por_categoria(cliente.Id_cliente)

        return {"categorias": contagem}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
@router_carrinho.delete("/item/{id_item}", response_model=CarrinhoOutSchema)
async def remover_item(
    id_item: Annotated[int, Path(..., description="ID do item a ser removido")],
    current_user: User = Depends(get_current_user)
):
    """
    Remove um item do carrinho
    """
    cliente = cliente_service.obter_cliente_por_email(current_user.username)
    try:
        return service_carrinho.remover_item(cliente.Id_cliente, id_item)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router_carrinho.put("/item/{id_item}", response_model=CarrinhoOutSchema)
async def atualizar_quantidade_item(
    id_item: Annotated[int, Path(..., description="ID do item a ser atualizado")],
    quantidade: Annotated[int, Path(..., gt=0, description="Nova quantidade")],
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza a quantidade de um item no carrinho
    """
    cliente = cliente_service.obter_cliente_por_email(current_user.username)
    try:
        return service_carrinho.atualizar_item(cliente.Id_cliente, id_item, quantidade)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router_carrinho.put("/", response_model=CarrinhoOutSchema)
async def atualizar_carrinho(
    carrinho_data: CarrinhoUpdateSchema,
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza todo o carrinho
    """

    try:
        return service_carrinho.atualizar_carrinho_completo(
            cliente_service.obter_cliente_por_email(current_user.username).Id_cliente,
            [item for item in carrinho_data.itens]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router_carrinho.delete("/limpar", status_code=status.HTTP_204_NO_CONTENT)
async def limpar_carrinho(current_user: User = Depends(get_current_user)):
    cliente = cliente_service.obter_cliente_por_email(current_user.username)
    """
    Limpa todos os itens do carrinho
    """
    try:
        service_carrinho.limpar_carrinho(cliente.Id_cliente)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
@router.get("/estoque")
@limiter.limit("10/minute")
async def listar_estoque(request: Request):
    return service.listar_estoque()

@router.post("/estoque/{produto}/alterar")
@limiter.limit("5/minute")
async def alterar_estoque(request: Request, produto: str, acao: str, quantity: int):
    estoque = service.listar_estoque()
    ingrediente_service = IngredienteService()
    if not estoque:
        raise HTTPException(status_code=400, detail="Estoque vazio")
    if ingrediente_service.get_by_name(nome_ingred=produto) is None:
        raise HTTPException(status_code=404, detail="Item inexistente")
    if acao == "adicionar":
        ingrediente_service.ajustar_estoque(produto, quantity)
    elif acao == "remover":
        if not estoque:
            raise HTTPException(status_code=400, detail="Estoque já está zerado")
        ingrediente_service.ajustar_estoque(produto, - quantity)
    else:
        raise HTTPException(status_code=400, detail="Ação inválida")

    return ingrediente_service.get_by_name(nome_ingred=produto)


# Authentication endpoints
@auth_router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
        request: Request,
        user_data: UserLogin
):
    """
    Autentica um usuário (cliente ou funcionário) e retorna token JWT

    - **username**: E-mail do usuário
    - **password**: Senha do usuário
    """
    try:
        # Autentica usando SecurityManager que verifica clientes e funcionários
        user_info = security.authenticate_user(user_data.username, user_data.password)
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Gera token com informações do usuário
        access_token = security.create_access_token(user_info)
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno durante autenticação"
        )


@auth_router.get("/me", response_model=UserOut)
async def read_users_me(
        current_user: Dict = Depends(security.get_current_user)
) -> UserOut:
    """
    Retorna informações do usuário autenticado
    """
    return UserOut(username=current_user.get("sub"), id = current_user.get("user_id"))


@auth_router.get("/funcionarios/login", response_model=Token)
@limiter.limit("5/second")
async def login_funcionario(
        request: Request,
        id_pass: int,
        password: str,
):
    """
    Autentica um funcionário por e-mail e senha

    - **email**: E-mail do funcionário
    - **password**: Senha do funcionário
    """
    try:
        # Tenta autenticar como funcionário
        user_info = security.authenticate_user(str(id_pass), password)

        if not user_info:
            logger.warning(f"Falha na autenticação para funcionário: {id_pass}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais de funcionário inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verifica explicitamente o tipo de usuário
        if user_info.get("user_type") != "funcionario":
            logger.warning(
                f"Tentativa de login como funcionário com credenciais de cliente: {id_pass}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais de funcionário inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Gera o token de acesso
        access_token = security.create_access_token(user_info)

        if not access_token:
            logger.error(f"Falha ao gerar token para funcionário: {id_pass}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao gerar token de acesso"
            )

        # Retorna no formato correto para o schema Token
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no login de funcionário: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno durante autenticação de funcionário"
        )


@auth_router.post("/register", response_model=Token)
@limiter.limit("5/minute")
async def register(
        request: Request,
        user_data: UserLogin):
    """
    Registra um novo usuário administrador

    - **username**: Nome de usuário
    - **password**: Senha
    """
    user_service = UserService()
    try:
        # Verifica se usuário já existe
        if user_service.get_user(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Usuário já existe",
            )

        # Cria novo usuário
        created_user = user_service.create_user(UserCreate(
            username=user_data.username,
            password=user_data.password
        ))

        # Prepara informações para token
        user_info = {
            "username": created_user.username,
            "user_type": "admin",
            "user_id": created_user.id
        }

        # Gera token
        access_token = security.create_access_token(user_info)
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no registro: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao registrar usuário"
        )

@router.post("/order/create")
@limiter.limit("5/minute")
async def register(request: Request, order: CreateOrder):
    service.create_order(order)
    return {"status": "created"}
@router.post("/order/all")
@limiter.limit("500/minute")
async def register(request: Request):
    return service.get_orders()


@auth_router.post("/token", response_model=Token)
@limiter.limit("5/minute")
async def login_with_form(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autentica um usuário usando formulário OAuth2 e retorna token JWT

    - **username**: E-mail do usuário
    - **password**: Senha do usuário
    """
    try:
        # Autentica o usuário (verifica cliente e funcionário)
        user_info = security.authenticate_user(form_data.username, form_data.password)

        if not user_info:
            logger.warning(f"Falha na autenticação para: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Gera token com informações completas do usuário
        access_token = security.create_access_token(user_info)
        logger.info(f"Token gerado para: {form_data.username} ({user_info['user_type']})")

        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na autenticação via formulário: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno durante autenticação"
        )



# Integration endpoints
@router.get("/")
@limiter.limit("10/minute")
async def get_items(request: Request):
    service.get_all_items()
    return {"status": "received"}
@router.delete("/")
@limiter.limit("10/minute")
async def get_item(request: Request, item: ItemDelete):
    service.delete(item)
    return {"status": "deleted"}


@router.post("/")
@limiter.limit("5/minute")
async def create_item(
    request: Request,
    item: ItemCreate,
):
    service.create_item(item)
    return {"status": "received"}
@router.put("/{item_id}")
@limiter.limit("5/minute")
async def update_item(
    request: Request,
    item: ItemUpdate,
):
    service.update_item(item)
    return {"status": "received"}

#################################### Pedidos ####################################

pedidoService = PedidoService()


@router.post("/pedido/", response_model=int, status_code=status.HTTP_201_CREATED)
def criar_pedido(pedido: PedidoCreate):
    pedido_id = pedidoService.criar_pedido(pedido)
    print(pedido_id)
    # Converte a string da data para objeto date se necessário
    data_pedido = pedido.Data_pedido if isinstance(pedido.Data_pedido, date) else date.fromisoformat(str(pedido.Data_pedido))

    totalizador_diario.adicionar_pedido(pedido.Valor_total_pedido, data_pedido)

    return pedido_id.Id_pedido


@router.get("/pedido/", response_model=List[PedidoOut])
def listar_pedidos():
    return pedidoService.listar_pedidos()


@router.get("/pedido/{pedido_id}", response_model=PedidoOut)
def obter_pedido(pedido_id: int):
    pedido = pedidoService.buscar_pedido_por_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


@router.put("/pedido/{pedido_id}", response_model=bool)
def atualizar_pedido(pedido_id: int, dados: PedidoUpdate):
    atualizado = pedidoService.atualizar_pedido(pedido_id, dados.model_dump(exclude_unset=True))
    if not atualizado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado ou sem alterações")
    return True


@router.delete("/pedido/{pedido_id}", response_model=bool)
def deletar_pedido(pedido_id: int):
    deletado = pedidoService.deletar_pedido(pedido_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return True
@router.get("/pedido/total-hoje/")
def obter_total_hoje():
    return {"total": totalizador_diario.obter_total_hoje()}

@router.get("/pedido/total-por-data/{data}")
def obter_total_por_data(data: str):
    try:
        data_consulta = date.fromisoformat(data)
        return {
            "data": data,
            "total": totalizador_diario.obter_total_por_data(data_consulta)
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD")