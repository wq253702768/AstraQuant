from datetime import UTC, datetime, timedelta
from typing import Any
import bcrypt
import jwt
from .errors import AppError, ErrorCode

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def create_jwt(subject: str, secret: str, expires_seconds: int, claims: dict[str, Any] | None = None) -> str:
    now = datetime.now(UTC)
    payload = {"sub": subject, "iat": int(now.timestamp()), "exp": int((now + timedelta(seconds=expires_seconds)).timestamp()), **(claims or {})}
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_jwt(token: str, secret: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise AppError(ErrorCode.UNAUTHORIZED, "Token 已过期", 401) from exc
    except jwt.PyJWTError as exc:
        raise AppError(ErrorCode.UNAUTHORIZED, "Token 无效", 401) from exc
