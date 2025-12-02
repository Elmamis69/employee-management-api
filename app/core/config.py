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

settings = Settings()