import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Carga las variables desde .env
load_dotenv()

@dataclass
class Settings:
    app_name: str = "Employee Management API"
    environment: str = os.getenv("ENVIRONMENT", "dev")
    database_url: str = os.getenv("DATABASE_URL")

    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int (os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

settings = Settings()