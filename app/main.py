from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from app.core.config import settings
from app.api.v1.routes_auth import router as auth_router

from app.api.v1.routes_employees import router as employees_router # nuevo import

# from app.db.session import Base, engine # Importa tu base y enginge
# from app.models import user, employee, activity_log # No se usan directo, pero registran los modelos

app = FastAPI (
    title = "Employee Management API",
    version = "0.1.0",
)

# Centralized exception hadlers
logger = logging.getLogger("uvicorn.error")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning("HTTPException: %s path = %s", exc.detail, request.url.path)
    return JSONResponse({"detail": exc.detail}, status_code = exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Return validation errors in a consistent JSON shape
    logger.info("Request validation error on %s: %s", request.url.path, exc.errors())
    return JSONResponse({"detail": exc.errors()}, status_code = 422)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Catch-all for unexpected exceptions (avoid exposing internals in responses)
    logger.error("Unhandled exception at %s: %s", request.url.path, exc, exc_info = exc)
    return JSONResponse({"detail": "Internal server error"}, status_code = 500)

# @app.on_event("startup")
# def on_startup() -> None:
#     # Temporalmente, hasta usar Alembic:
#     Base.metadata.create_all(bind = engine)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "environment": settings.environment}

# API v1 routers
app.include_router(auth_router, prefix = "/api/v1")
app.include_router(employees_router, prefix = "/api/v1")