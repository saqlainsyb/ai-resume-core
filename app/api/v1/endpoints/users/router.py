from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.api.v1.endpoints.users import schemas, service
from app.api.v1.endpoints.auth.utils import get_current_user
from app.api.v1.endpoints.auth.models import User

router = APIRouter()

@router.get("/me", response_model=schemas.UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserOut)
async def update_me(user_update: schemas.UserUpdate, current_user: User = Depends(get_current_user)):
    async with async_session() as session:
        updated_user = await service.update_user(session, current_user.id, user_update)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated_user
