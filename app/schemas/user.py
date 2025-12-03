from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.EMPLOYEE
    is_active: bool = True

class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None