from fastapi import FastAPI

from app.core.config import settings

app = FastAPI (
    title = "Employee Management API",
    version = "0.1.0",
)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "environment": settings.environment}