#tests/test/auth.py
import pytest

def test_login_success(client, admin_token):
    """
    Test: Login exitoso con credenciales correctas
    Esperado: 200 OK y devuelve un access_token
    """
    response = client.post(
        "/api/v1/auth/login",
        data = {"username": "admin@example.com", "password": "hola123123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client, admin_user):
    """
    Test: Login con contraseña incorrecta
    Esperado: 401 Unauthorized
    """
    response = client.post(
        "/api/v1/auth/login",
        data = {"username": "admin@example.com", "password": "contraseña_incorrecta"},
    )

    assert response.status_code == 401
    assert "detail" in response.json()

def test_login_user_not_found(client):
    """
    Test: Login con usuario que no existe
    Esperado: 401 Unauthorized
    """
    response = client.post(
        "/api/v1/auth/login",
        data = {"username": "noexiste@example.com", "password": "cualquier_password"},
    )

    assert response.status_code == 401
    assert "detail" in response.json()

def test_login_missing_fields(client):
    """
    Test: Login sin enviar username o password
    Esperado: 422 Unprocessable Entity (error de validacion)
    """
    response = client.post(
        "/api/v1/auth/login",
        data = {"username": "admin@example.com"}, # falta password
    )

    assert response.status_code == 422
    assert "detail" in response.json()