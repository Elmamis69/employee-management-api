from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps_auth import get_user_by_email
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.db.deps import get_db
from app.models.user import User, UserRole
from app.schemas.user import Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])

DBSession = Annotated[Session, Depends(get_db)]

@router.post("/register", response_model=UserRead, status_code = status.HTTP_201_CREATED)
def register_user(
    payload: UserCreate,
    db: DBSession,
) -> User:
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user = User(
        email = payload.email,
        full_name = payload.full_name,
        hashed_password = get_password_hash(payload.password),
        role = UserRole.ADMIN, # opcional: el primero admin, luego podemos cambiar la logica
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model = Token)
def login (
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DBSession,
) -> Token:
    user = get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Incorrect email or password",
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Incorrect email or password",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Inactive user",
        )
    
    access_token = create_access_token(subject = user.email)
    return Token(access_token = access_token)