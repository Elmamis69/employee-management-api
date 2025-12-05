# tests/test_employees.py
import pytest


def test_create_employee_success(client, admin_token):
    """
    Test: Crear empleado exitosamente con token válido
    Esperado: 201 Created y retorna datos del empleado
    """
    response = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "juan.perez@example.com",
            "department": "IT",
            "position": "Developer",
            "is_active": True,
            "hired_at": "2025-01-01",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Juan"
    assert data["last_name"] == "Pérez"
    assert data["email"] == "juan.perez@example.com"
    assert data["id"] is not None


def test_create_employee_unauthorized(client):
    """
    Test: Intentar crear empleado sin token
    Esperado: 401 Unauthorized
    """
    response = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "juan.perez@example.com",
            "department": "IT",
            "position": "Developer",
            "is_active": True,
            "hired_at": "2025-01-01",
        },
    )
    
    assert response.status_code == 401
    assert "detail" in response.json()


def test_create_employee_duplicate_email(client, admin_token):
    """
    Test: Intentar crear empleado con email duplicado
    Esperado: 400 Bad Request
    """
    # Crear primer empleado
    client.post(
        "/api/v1/employees",
        json={
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "juan.perez@example.com",
            "department": "IT",
            "position": "Developer",
            "is_active": True,
            "hired_at": "2025-01-01",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    # Intentar crear otro con el mismo email
    response = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Otro",
            "last_name": "Usuario",
            "email": "juan.perez@example.com",
            "department": "HR",
            "position": "Manager",
            "is_active": True,
            "hired_at": "2025-01-15",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_list_employees(client, admin_token):
    """
    Test: Listar empleados activos
    Esperado: 200 OK y retorna lista (puede estar vacía)
    """
    response = client.get(
        "/api/v1/employees",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_employees_with_pagination(client, admin_token):
    """
    Test: Listar empleados con parámetros de paginación
    Esperado: 200 OK respeta skip y limit
    """
    response = client.get(
        "/api/v1/employees?skip=0&limit=10",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_get_employee_success(client, admin_token):
    """
    Test: Obtener empleado por ID
    Esperado: 200 OK y retorna datos del empleado
    """
    # Crear empleado primero
    create_response = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Carlos",
            "last_name": "López",
            "email": "carlos.lopez@example.com",
            "department": "Finance",
            "position": "Accountant",
            "is_active": True,
            "hired_at": "2025-02-01",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    employee_id = create_response.json()["id"]
    
    # Obtener empleado
    response = client.get(
        f"/api/v1/employees/{employee_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == employee_id
    assert data["first_name"] == "Carlos"


def test_get_employee_not_found(client, admin_token):
    """
    Test: Obtener empleado con ID que no existe
    Esperado: 404 Not Found
    """
    response = client.get(
        "/api/v1/employees/9999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_employee_success(client, admin_token):
    """
    Test: Actualizar datos de un empleado
    Esperado: 200 OK y retorna empleado actualizado
    """
    # Crear empleado
    create_response = client.post(
        "/api/v1/employees",
        json={
            "first_name": "María",
            "last_name": "González",
            "email": "maria.gonzalez@example.com",
            "department": "HR",
            "position": "Recruiter",
            "is_active": True,
            "hired_at": "2025-03-01",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    employee_id = create_response.json()["id"]
    
    # Actualizar empleado
    response = client.put(
        f"/api/v1/employees/{employee_id}",
        json={
            "department": "Management",
            "position": "HR Manager",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == employee_id
    assert data["department"] == "Management"
    assert data["position"] == "HR Manager"


def test_update_employee_not_found(client, admin_token):
    """
    Test: Intentar actualizar empleado que no existe
    Esperado: 404 Not Found
    """
    response = client.put(
        "/api/v1/employees/9999",
        json={"department": "IT"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_employee_success(client, admin_token):
    """
    Test: Eliminar (soft delete) un empleado
    Esperado: 204 No Content
    """
    # Crear empleado
    create_response = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Laura",
            "last_name": "Martínez",
            "email": "laura.martinez@example.com",
            "department": "Sales",
            "position": "Sales Rep",
            "is_active": True,
            "hired_at": "2025-04-01",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    employee_id = create_response.json()["id"]
    
    # Eliminar empleado
    response = client.delete(
        f"/api/v1/employees/{employee_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 204


def test_delete_employee_not_found(client, admin_token):
    """
    Test: Intentar eliminar empleado que no existe
    Esperado: 404 Not Found
    """
    response = client.delete(
        "/api/v1/employees/9999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_inactive_employees(client, admin_token):
    """
    Test: Listar empleados inactivos (soft deleted)
    Esperado: 200 OK y retorna lista de inactivos
    """
    # Crear y eliminar un empleado
    create_response = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Test",
            "last_name": "Inactivo",
            "email": "test.inactivo@example.com",
            "department": "Test",
            "position": "Test",
            "is_active": True,
            "hired_at": "2025-05-01",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    employee_id = create_response.json()["id"]
    
    # Eliminar
    client.delete(
        f"/api/v1/employees/{employee_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    # Listar inactivos
    response = client.get(
        "/api/v1/employees?is_active=false",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # El empleado eliminado debe estar en la lista
    assert any(emp["id"] == employee_id for emp in data)


def test_create_employee_invalid_data(client, admin_token):
    """
    Test: Crear empleado con datos inválidos (missing required fields)
    Esperado: 422 Unprocessable Entity
    """
    response = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Incompleto",
            # falta last_name
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 422
    assert "detail" in response.json()
