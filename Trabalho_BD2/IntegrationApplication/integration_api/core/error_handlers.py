from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback

logger = logging.getLogger(__name__)

def register_handlers(app):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"HTTP error {exc.status_code} on {request.url}: {exc.detail!r}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "path": str(request.url),
                "type": "http_exception",
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation failed on {request.url}: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation failed",
                "details": exc.errors(),
                "path": str(request.url),
                "body": await request.body(),
                "type": "validation"
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        tb = traceback.format_exc()
        logger.error(f"Unexpected error on {request.url}: {str(exc)}\n{tb}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "exception": str(exc),
                "traceback": tb,
                "path": str(request.url),
                "type": "server_error"
            }
        )