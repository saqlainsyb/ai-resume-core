from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.api.v1.endpoints.resumes import schemas, service
from app.api.v1.endpoints.auth.utils import get_current_user
from app.api.v1.endpoints.auth.models import User

router = APIRouter()

@router.post("/", response_model=schemas.ResumeOut)
async def create_resume(resume: schemas.ResumeCreate, current_user: User = Depends(get_current_user)):
    async with async_session() as session:
        return await service.create_resume(session, resume, current_user.id)

@router.get("/{resume_id}", response_model=schemas.ResumeOut)
async def read_resume(resume_id: int, current_user: User = Depends(get_current_user)):
    async with async_session() as session:
        resume = await service.get_resume(session, resume_id, current_user.id)
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
        return resume

@router.get("/", response_model=list[schemas.ResumeOut])
async def read_resumes(current_user: User = Depends(get_current_user)):
    async with async_session() as session:
        return await service.get_resumes(session, current_user.id)

@router.put("/{resume_id}", response_model=schemas.ResumeOut)
async def update_resume(resume_id: int, resume: schemas.ResumeUpdate, current_user: User = Depends(get_current_user)):
    async with async_session() as session:
        updated_resume = await service.update_resume(session, resume_id, current_user.id, resume)
        if not updated_resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
        return updated_resume

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(resume_id: int, current_user: User = Depends(get_current_user)):
    async with async_session() as session:
        success = await service.delete_resume(session, resume_id, current_user.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
