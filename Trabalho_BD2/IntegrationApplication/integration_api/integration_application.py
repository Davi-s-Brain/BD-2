from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from Trabalho_BD2.IntegrationApplication.integration_api.api.routes import router as integration_router, auth_router  # Adicionando auth_router
from Trabalho_BD2.IntegrationApplication.integration_api.core.db import init_db
from Trabalho_BD2.IntegrationApplication.integration_api.core.error_handlers import register_handlers
from Trabalho_BD2.IntegrationApplication.integration_api.core.limiter import limiter
from Trabalho_BD2.IntegrationApplication.integration_api.core.security_manager import SecurityManager
from slowapi.middleware import SlowAPIMiddleware

# Configuração do SecurityManager
SECURITY = SecurityManager()

def create_app() -> FastAPI:
    app = FastAPI(title="Integration API")
    origins = [
        "http://localhost:5500",  # coloque aqui o endereço/porta do seu front
        "http://localhost:3000",  # adicione outras origens se usar
        "http://localhost:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Middleware
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    # Incluir os routers
    app.include_router(integration_router)
    app.include_router(auth_router)  # Adicionando o router de autenticação
    register_handlers(app)

    # Inicializar o banco de dados
    init_db()

    return app

app = create_app()