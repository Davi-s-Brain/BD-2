from datetime import date
from typing import List, Dict, Any, Annotated

from fastapi import APIRouter, Request, Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from Trabalho_BD2.IntegrationApplication.integration_api.core.limiter import limiter
from Trabalho_BD2.IntegrationApplication.integration_api.core.security_manager import SecurityManager
from Trabalho_BD2.IntegrationApplication.integration_api.core.totalizador import totalizador_diario
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.carrinho_schemas import (
    ItemCarrinhoSchema,
    CarrinhoOutSchema,
    CarrinhoUpdateSchema, ContagemCategoriasOutSchema
)
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.funcionario import (
    FuncionarioCreate,
    FuncionarioUpdate,
    FuncionarioOut,
)
from Trabalho_BD2.IntegrationApplication.integration_api.services.cliente_service import ClienteService
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.cliente_schemas import (
    ClienteCreate,
    ClienteUpdate,
    ClienteOut
)
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.ingrediente_schemas import IngredienteOut, \
    IngredienteCreate, IngredienteUpdate
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.item import ItemCreate, ItemUpdate, ItemDelete
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.order import CreateOrder
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoOut
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.user import UserLogin, Token, User
from Trabalho_BD2.IntegrationApplication.integration_api.services.carrinho_service import CarrinhoService
from Trabalho_BD2.IntegrationApplication.integration_api.services.funcionario_service import FuncionarioService
from Trabalho_BD2.IntegrationApplication.integration_api.services.ingrediente_service import IngredienteService
from Trabalho_BD2.IntegrationApplication.integration_api.services.item_service import ItemService
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
# Configuração do router
cliente_router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
)

cliente_service = ClienteService()


@cliente_router.post(
    "/",
    response_model=Token,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("5/minute")
async def criar_cliente(request: Request, cliente: ClienteCreate):
    """
    Cria um novo cliente
    """
    try:
        db_cliente = cliente_service.criar_cliente(cliente)
        security.create_user(str(db_cliente.E_mail_client),db_cliente.Senha_cliente)
        access_token = security.create_access_token(data={"sub": db_cliente.E_mail_client})
        print("O token gerado foi" + access_token)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as http_exc:
        raise http_exc  # já é estruturado, pode propagar
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao criar cliente"
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
    new_id = ingredienteService.create(
        Tipo_ingred=data.Tipo_ingred,
        Nome_ingred=data.Nome_ingred,
        Preco_venda_cliente=data.Preco_venda_cliente,
        Peso_ingred=data.Peso_ingred,
        Indice_estoq=data.Indice_estoq,
        Quantidade = data.Quantidade
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

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = security.get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(**user)


router_carrinho = APIRouter(prefix="/carrinho", tags=["Carrinho"])
service_carrinho = CarrinhoService()

@router_carrinho.get("/", response_model=CarrinhoOutSchema)
async def obter_carrinho(token: str = Depends(oauth2_scheme), current_user: User = Depends(get_current_user)):
    """
    Obtém o carrinho do usuário atual
    """
    print(current_user.username)
    try:
        cliente = cliente_service.obter_cliente_por_email(current_user.username)
        print(current_user.username)
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
            current_user.id,
            [item.model_dump() for item in carrinho_data.itens]
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
    if ingrediente_service.get_by_name(Nome_ingred=produto) is None:
        raise HTTPException(status_code=404, detail="Item inexistente")
    if acao == "adicionar":
        ingrediente_service.alterar_estoque(produto, quantity)
    elif acao == "remover":
        if not estoque:
            raise HTTPException(status_code=400, detail="Estoque já está zerado")
        ingrediente_service.alterar_estoque(produto, - quantity)
    else:
        raise HTTPException(status_code=400, detail="Ação inválida")

    return ingrediente_service.get_by_name(Nome_ingred=produto)

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
    print(pedido)
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