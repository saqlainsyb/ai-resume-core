# app/api/v1/endpoints/auth/router.py
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.v1.endpoints.auth.schemas import UserCreate, UserLogin, UserOut, Token
from app.api.v1.endpoints.auth.models import User
from app.api.v1.endpoints.auth.service import get_password_hash, verify_password, create_access_token
from app.api.v1.endpoints.auth.utils import oauth2_scheme, get_current_user
from app.db.session import async_session
from app.core.config import settings
from app.utils import form_data_as

router = APIRouter()

@router.post("/register", response_model=UserOut, tags=["Authentication"])
async def register(user_in: UserCreate):
    async with async_session() as session:
        # Check if a user with the same email already exists.
        query = select(User).where(User.email == user_in.email)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        # Create new user with hashed password.
        new_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password)
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

@router.post("/login", response_model=Token, tags=["Authentication"])
async def login(user_in: UserLogin = Depends(form_data_as(UserLogin))):
    async with async_session() as session:
        # query = select(User).where(User.email == user_in.email) # Let's use this in prod
        query = select(User).where(User.username == user_in.username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user or not verify_password(user_in.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

# Example: A protected endpoint to test token validity.
@router.get("/me", response_model=UserOut, tags=["Authentication"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
