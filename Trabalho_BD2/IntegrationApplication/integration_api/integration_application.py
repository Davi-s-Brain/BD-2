from fastapi import FastAPI
from Trabalho_BD2.IntegrationApplication.integration_api.api.routes import router as integration_router
from Trabalho_BD2.IntegrationApplication.integration_api.core.db import init_db
from Trabalho_BD2.IntegrationApplication.integration_api.core.error_handlers import register_handlers
from Trabalho_BD2.IntegrationApplication.integration_api.core.limiter import limiter
from Trabalho_BD2.IntegrationApplication.integration_api.core.security_manager import SecurityManager
from slowapi.middleware import SlowAPIMiddleware

# Configuração do SecurityManager
SECURITY = SecurityManager()


def create_app() -> FastAPI:
    app = FastAPI(title="Integration API")

    # Middleware
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    # Incluir o router
    app.include_router(integration_router)
    register_handlers(app)

    # Inicializar o banco de dados
    init_db()

    return app


app = create_app()
