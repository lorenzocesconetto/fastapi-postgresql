from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(*, plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def create_access_token(subject: str, expires_delta: timedelta | None = None, **kwargs) -> str:
    if not isinstance(subject, str):
        raise ValueError("Subject must be a string")
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {**kwargs, "exp": expire.timestamp(), "sub": subject, "nbf": now, "iat": now}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_SIGNATURE_ALGORITHM
    )
    return encoded_jwt


def generate_password_reset_token(email: EmailStr) -> str:
    return create_access_token(
        subject=email,
        expires_delta=timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS),
    )


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.TOKEN_SIGNATURE_ALGORITHM]
        )
        return decoded_token["email"]
    except jwt.JWTError:
        return None
