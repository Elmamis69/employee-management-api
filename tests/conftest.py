import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.deps import get_db
from app.db.session import Base
from app.models.user import User, UserRole
from app.core.security import get_password_hash

# Configurar BD en memoria para tests (SQLite)
@pytest.fixture(scope="session")
def db_engine():
    """Crear motor de BD SQLite en memoria (persiste durante toda la sesion de tests). """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Crear todas las tablas basadas en los modelos
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata

@pytest.fixture
def db_session(db_engine):
    """Crear una sesion de BD para cada test (transaccion aislada)"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit = False, autoflush = False, bind = connection)(
        bind = connection
    )

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Inyecta la sesion de test en la dependencia get_db de FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    # Limpiar overrides despues del set
    app.dependency_overrides.clear()

@pytest.fixture
def admin_user(db_session):
    """Crea un usuario admin en la BD de tests"""
    admin = User(
        email = "admin@example.com",
        hashed_password = get_password_hash("hola123123"),
        full_name = "Admin User",
        is_active = True,
        role = UserRole.ADMIN,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture
def admin_token(client, admin_user):
    """Obtiene un token JWT para el usuario admin"""
    response = client.post(
        "/api/v1/auth/login",
        data = { "username": "admin@example.com", "password": "hola123123"},
    )
    return response.json()["access_token"] 