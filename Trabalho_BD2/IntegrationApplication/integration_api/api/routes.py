from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.item import ItemCreate, ItemUpdate
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.order import CreateOrder
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.user import UserLogin, Token, User
from Trabalho_BD2.IntegrationApplication.integration_api.services.item_service import ItemService
from Trabalho_BD2.IntegrationApplication.integration_api.core.limiter import limiter
from Trabalho_BD2.IntegrationApplication.integration_api.core.security_manager import SecurityManager

security = SecurityManager()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Routers
router = APIRouter(prefix="/integration", tags=["Integration"])
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
service = ItemService()

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

@auth_router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Integration endpoints
@router.get("/")
@limiter.limit("10/minute")
async def get_items(request: Request):
    service.get_all_items()
    return {"status": "received"}

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
    current_user: User = Depends(get_current_user)
):
    service.update_item(item)
    return {"status": "received"}
