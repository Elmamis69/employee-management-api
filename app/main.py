from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.routes_auth import router as auth_router

from app.api.v1.routes_employees import router as employees_router # nuevo import

# from app.db.session import Base, engine # Importa tu base y enginge
# from app.models import user, employee, activity_log # No se usan directo, pero registran los modelos

app = FastAPI (
    title = "Employee Management API",
    version = "0.1.0",
)

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