from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.endpoints.auth.models import User
from sqlalchemy.future import select
from app.api.v1.endpoints.users.schemas import UserUpdate

async def get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def update_user(session: AsyncSession, user_id: int, user_update: UserUpdate):
    user = await get_user_by_id(session, user_id)
    if user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)
    return user
