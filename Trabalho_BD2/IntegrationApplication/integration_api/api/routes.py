from fastapi import APIRouter, Request, Depends
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.item import ItemCreate, ItemUpdate
from Trabalho_BD2.IntegrationApplication.integration_api.services.item_service import ItemService
from Trabalho_BD2.IntegrationApplication.integration_api.core.limiter import limiter
from Trabalho_BD2.IntegrationApplication.integration_api.core.security_manager import SecurityManager

security = SecurityManager()

router = APIRouter(prefix="/integration", tags=["Integration"])
service = ItemService()

def require_auth(request: Request):
    security.validate(request)

@router.get("/", dependencies=[Depends(require_auth)])
@limiter.limit("10/minute")
def get_items(request: Request):
    service.get_all_items()
    return {"status": "received"}

@router.post("/", dependencies=[Depends(require_auth)])
@limiter.limit("5/minute")
def create_item(item: ItemCreate, request: Request):
    service.create_item(item)
    return {"status": "received"}

@router.put("/{item_id}", dependencies=[Depends(require_auth)])
@limiter.limit("5/minute")
def update_item(item_id: int, item: ItemUpdate, request: Request):
    service.update_item(item_id, item)
    return {"status": "received"}
