from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps_auth import require_roles
from app.db.deps import get_db
from app.models.employee import Employee
from app.models.user import User, UserRole
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate
)
from app.core.logging import create_activity # import para logging

router = APIRouter(prefix = "/employees", tags = ["Employees"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentAdminOrManager = Annotated [
    User,
    Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER)),
]

@router.post(
    "",
    response_model = EmployeeRead,
    status_code = status.HTTP_201_CREATED
)
def create_employee(
    payload: EmployeeCreate,
    db: DBSession,
    current_user: CurrentAdminOrManager,
) -> Employee:
    # opcional: validar email unico si viene
    if payload.email:
        existing_stmt = select(Employee).where(Employee.email == payload.email)
        existing = db.scalar(existing_stmt)
        if existing:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Employee with this email already exists",
            )
    
    employee = Employee(
        first_name = payload.first_name,
        last_name = payload.last_name,
        email = payload.email,
        department = payload.department,
        position = payload.position,
        is_active = payload.is_active,
        hired_at = payload.hired_at,
        created_by_id = current_user.id,
    )
    db.add(employee)
    db.flush() # Obtiene el ID del empleado sin hacer commit aun
    create_activity(
        db = db,
        user = current_user,
        action = "create_employee",
        resource_type = "employee",
        resource_id = (employee.id),
        details = f"Created employee {employee.first_name} {employee.last_name} {employee.id})"
    )
    db.commit()
    db.refresh(employee)
    return employee
    
@router.get("", response_model = List[EmployeeRead])
def list_employeess(
    db: DBSession,
    current_user: CurrentAdminOrManager,
    is_active: bool = Query(True, description = "Filter by active status"),
    skip: int = Query(0, ge = 0),
    limit: int = Query(20, ge = 1, le = 100),
) -> list [Employee]:
    stmt = (
        select(Employee)
        .where(Employee.is_active == is_active)
        .order_by(Employee.id)
        .offset(skip)
        .limit(limit)
    )
    employees = db.scalars(stmt).all()
    return employees

def _get_employee_or_404(employee_id: int, db: Session) -> Employee:
    stmt = select(Employee).where(Employee.id == employee_id)
    employee = db.scalar(stmt)
    if employee is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Employee not found",
        )
    return employee

@router.get("/{employee_id}", response_model = EmployeeRead)
def get_employee(
    employee_id: int,
    db: DBSession,
    current_user: CurrentAdminOrManager,
) -> Employee:
    return _get_employee_or_404(employee_id, db)

@router.put("/{employee_id}", response_model = EmployeeRead)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    db: DBSession,
    current_user: CurrentAdminOrManager,
) -> Employee:
    employee = _get_employee_or_404(employee_id, db)

    update_data = payload.model_dump(exclude_unset = True)

    for field, value in update_data.items():
        setattr(employee, field, value)

    db.add(employee)
    create_activity(
        db = db,
        user = current_user,
        action = "update_employee",
        resource_type = "employee",
        resource_id = str(employee.id),
        details = f"Updated employee: {', '.join(update_data.keys())} "
    )
    db.commit()
    db.refresh(employee)
    return employee

@router.delete(
    "/{employee_id}",
    status_code = status.HTTP_204_NO_CONTENT,
)
def delete_employee(
    employee_id: int,
    db: DBSession,
    current_user: CurrentAdminOrManager,
) -> None:
    employee = _get_employee_or_404(employee_id, db)

    # soft delete
    employee.is_active = False

    db.add(employee)
    create_activity(
        db = db,
        user = current_user,
        action = "delete_employee",
        resource_type = "employee",
        resource_id = str(employee.id),
        details = f"Soft deleted (is_active = False)"
    )
    db.commit()
    # 204 -> sin body