# app/api/v1/endpoints/auth/service.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError
from app.core.config import settings

# Setup password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(*, data: dict, expires_delta: timedelta = None) -> str:
    """Generates a JWT token using PyJWT with expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add expiration to the payload.
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
