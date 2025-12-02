from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine (
    settings.database_url,
    future=True,
)

SessionLocal = sessionmaker(
    bind = engine,
    autoflush = False,
    autocomit = False,
)

Base = declarative_base()
