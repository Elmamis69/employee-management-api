from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.deps import get_db
from app.schemas.user import TokenData

from app.models.user import User, UserRole # Nuevo import para RBAC (helper para roles (ADMIN/MANAGER))
from typing import Callable # Nuevo import para RBAC (helper para roles (ADMIN/MANAGER))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return db.scalar(stmt)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Could not validate credentials",
            headers = {"WWW-Authenticate": "Bearer"},
        )

    token_data = TokenData(email=payload["sub"])
    if token_data.email is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Could not validate credentials",
            headers = {"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(db, token_data.email)
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "User not found",
            headers = {"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Inactive user",
        )
    return current_user

def require_roles(*roles : UserRole) -> Callable[[User], User]:
    """"
    Dependencia para restringir acceso segun rol.
    Uso:
        current_admin = Depends(require_roles(UserRole.ADMIN))
        current_manager_or_admin = Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))
    """
    def role_checker(current_user: User = Depends  (get_current_active_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "Insufficient permissions",
            )
        return current_user
    return role_checker
