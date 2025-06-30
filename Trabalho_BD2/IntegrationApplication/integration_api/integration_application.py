# main.py (ou integration_application.py)
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.routes import router as integration_router, auth_router, func_router, ingrediente_router, router_carrinho, \
    cliente_router, combo_router, ambiente_router
from .core.db import DatabaseManager  # Importe o DatabaseManager
from .core.error_handlers import register_handlers
from .core.limiter import limiter
from .core.security_manager import SecurityManager
from slowapi.middleware import SlowAPIMiddleware
import traceback

SECURITY = SecurityManager()


def create_app() -> FastAPI:
    app = FastAPI(title="Integration API")

    # Configuração CORS
    origins = [
        "http://localhost:5500",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    app.include_router(integration_router)
    app.include_router(combo_router)
    app.include_router(func_router)
    app.include_router(router_carrinho)
    app.include_router(ingrediente_router)
    app.include_router(cliente_router)
    app.include_router(ambiente_router)
    app.include_router(auth_router)
    register_handlers(app)

    @app.on_event("startup")
    def init_database():
        db_manager = DatabaseManager()
        db_manager.init_db()
        print("Banco de dados inicializado com sucesso")
    return app


app = create_app()