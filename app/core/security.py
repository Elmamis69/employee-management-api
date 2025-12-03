from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(
        subject: str,
        expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes = settings.access_token_expire_minutes)

        to_encode: dict[str, Any] = {
            "sub": subject,
            "exp": datetime.now(timezone.utc) + expires_delta,
        }

        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm = settings.algorithm,
        )
        return encoded_jwt
    
def decode_access_token(token: str) -> Optional[dict[str, Any]]:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        return payload
    except JWTError:
        return None