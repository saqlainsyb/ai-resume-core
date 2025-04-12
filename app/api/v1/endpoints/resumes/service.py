from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.v1.endpoints.resumes.models import Resume
from app.api.v1.endpoints.resumes.schemas import ResumeCreate, ResumeUpdate

async def create_resume(session: AsyncSession, resume: ResumeCreate, user_id: int):
    new_resume = Resume(user_id=user_id, **resume.dict())
    session.add(new_resume)
    await session.commit()
    await session.refresh(new_resume)
    return new_resume

async def get_resume(session: AsyncSession, resume_id: int, user_id: int):
    result = await session.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def get_resumes(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(Resume).where(Resume.user_id == user_id)
    )
    return result.scalars().all()

async def update_resume(session: AsyncSession, resume_id: int, user_id: int, resume_data: ResumeUpdate):
    resume = await get_resume(session, resume_id, user_id)
    if resume:
        for key, value in resume_data.dict(exclude_unset=True).items():
            setattr(resume, key, value)
        await session.commit()
        await session.refresh(resume)
    return resume

async def delete_resume(session: AsyncSession, resume_id: int, user_id: int):
    resume = await get_resume(session, resume_id, user_id)
    if resume:
        await session.delete(resume)
        await session.commit()
        return True
    return False
