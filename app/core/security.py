from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt  # type: ignore
from passlib.context import CryptContext  # type: ignore

from app.core.config import settings
from app.core.exceptions import Unauthenticated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Jwt:
    @staticmethod
    def _encode_token(claims: dict[str, Any]) -> str:
        return jwt.encode(
            claims, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def _decode_token(token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError as e:
            raise Unauthenticated("Could not validate credentials")

    @classmethod
    async def get_access_token(cls, sub: Any) -> str:
        expire_time = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_IN_DAYS)
        expire = datetime.utcnow() + expire_time
        to_encode = {"sub": sub, "exp": expire}
        return cls._encode_token(to_encode)

    @classmethod
    async def decode_access_token(cls, token: str) -> dict[str, Any]:
        return cls._decode_token(token)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
