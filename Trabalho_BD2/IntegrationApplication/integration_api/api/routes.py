from datetime import date
from typing import List, Dict, Any

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from Trabalho_BD2.IntegrationApplication.integration_api.core.totalizador import totalizador_diario
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.ingrediente_schemas import IngredienteOut, \
    IngredienteCreate, IngredienteUpdate
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.item import ItemCreate, ItemUpdate, ItemDelete
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.order import CreateOrder, GetOrder
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoOut
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.user import UserLogin, Token, User
from Trabalho_BD2.IntegrationApplication.integration_api.services.funcionario_service import FuncionarioService
from Trabalho_BD2.IntegrationApplication.integration_api.services.ingrediente_service import IngredienteService
from Trabalho_BD2.IntegrationApplication.integration_api.services.item_service import ItemService
from Trabalho_BD2.IntegrationApplication.integration_api.core.limiter import limiter
from Trabalho_BD2.IntegrationApplication.integration_api.core.security_manager import SecurityManager
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.funcionario import (
    FuncionarioCreate,
    FuncionarioUpdate,
    FuncionarioOut,
)
from Trabalho_BD2.IntegrationApplication.integration_api.services.pedido import PedidoService

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

@ingrediente_router.post(
    "/",
    response_model=IngredienteOut,
    status_code=status.HTTP_201_CREATED
)
async def create_ingrediente(data: IngredienteCreate):
    """Cria um novo ingrediente"""
    new_id = ingredienteService.create(
        Tipo_ingred=data.Tipo_ingred,
        Nome_ingred=data.Nome_ingred,
        Preco_venda_cliente=data.Preco_venda_cliente,
        Peso_ingred=data.Peso_ingred,
        Indice_estoq=data.Indice_estoq
    )
    return ingredienteService.get_by_id(new_id)

@ingrediente_router.get(
    "/",
    response_model=List[Dict[str, Any]]
)
async def list_ingredientes():
    """Lista todos os ingredientes"""
    return ingredienteService.get_all()

@ingrediente_router.get(
    "/{ingrediente_id}",
    response_model=Dict[str, Any]
)
async def get_ingrediente(ingrediente_id: int):
    """Obtém um ingrediente específico pelo ID"""
    ingrediente = ingredienteService.get_by_id(ingrediente_id)
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
    dados_atualizacao = {k: v for k, v in data.dict(exclude_unset=True).items()}
    atualizado = ingredienteService.update(ingrediente_id, dados_atualizacao)
    if not atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não encontrado"
        )
    return ingredienteService.get_by_id(ingrediente_id)

@ingrediente_router.delete(
    "/{ingrediente_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_ingrediente(ingrediente_id: int):
    """Remove um ingrediente"""
    deleted = ingredienteService.delete(ingrediente_id)
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
    new_id = service.create(data)
    return funcService.get_by_id(new_id)

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
    return service.get_by_id(func_id)

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

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = security.get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(**user)
@router.get("/estoque")
@limiter.limit("10/minute")
async def listar_estoque(request: Request):
    return service.listar_estoque()

@router.post("/estoque/{produto}/alterar")
@limiter.limit("5/minute")
async def alterar_estoque(request: Request, produto: str, acao: str, quantity: int):
    estoque = service.listar_estoque()
    if not estoque:
        raise HTTPException(status_code=400, detail="Estoque vazio")
    if service.get_item(name=produto) is None:
        raise HTTPException(status_code=404, detail="Item inexistente")
    if acao == "adicionar":
        service.alterar_estoque(produto, quantity)
    elif acao == "remover":
        if not estoque:
            raise HTTPException(status_code=400, detail="Estoque já está zerado")
        service.alterar_estoque(produto, - quantity)
    else:
        raise HTTPException(status_code=400, detail="Ação inválida")

    return service.get_item(name=produto)

# Authentication endpoints
@auth_router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, user_data: UserLogin):
    user = security.authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
@auth_router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
@auth_router.get("/{func_id}", response_model=Token)
@limiter.limit("5/second")
async def login_funcionario(request: Request, func_id: int, password):
    func = funcService.get_by_id(func_id)
    if not func:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    if func.Senha_func != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": str(func_id)})
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print("Requisicao de entrada com o token"+ access_token)
    return {"access_token": access_token, "token_type": "bearer"}
@auth_router.post("/register", response_model=Token)
@limiter.limit("5/minute")
async def register(request: Request, user_data: UserLogin):
    # Verifica se o usuário já existe no banco de dados
    existing_user = security.authenticate_user(user_data.username,user_data.password)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já existe",
        )

    # Cria o novo usuário no banco de dados
    new_user = security.create_user(user_data.username, user_data.password)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar usuário",
        )

    # Autentica o novo usuário (opcional, mas útil para já retornar o token)
    access_token = security.create_access_token(data={"sub": user_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


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
async def login_with_form(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = security.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}



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
    pedido_id = pedidoService.criar_pedido(pedido.__dict__)

    # Converte a string da data para objeto date se necessário
    data_pedido = pedido.Data_pedido if isinstance(pedido.Data_pedido, date) else date.fromisoformat(str(pedido.Data_pedido))

    totalizador_diario.adicionar_pedido(pedido.Valor_total_pedido, data_pedido)

    return pedido_id


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
    atualizado = pedidoService.atualizar_pedido(pedido_id, dados.dict(exclude_unset=True))
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