from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    position: Optional[str] = None
    is_active: bool = True
    hired_at: Optional[date] = None

class EmployeeCreate(EmployeeBase):
    # en create no permitimos cambiar is_active, siempre True al inicio
    is_active: bool = True

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    position: Optional[str] = None
    is_active: Optional[bool] = None
    hired_at: Optional[date] = None

class EmployeeRead(EmployeeBase):
    id: int
    created_by_id: Optional[int] = None

    class Config:
        from_attributes = True