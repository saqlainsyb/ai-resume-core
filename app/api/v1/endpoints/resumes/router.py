from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.api.v1.endpoints.resumes import schemas, service
from app.api.v1.endpoints.auth.utils import get_current_user
from app.api.v1.endpoints.auth.models import User
# from app.core.templates import templates


router = APIRouter()

# @router.post("/", response_model=schemas.ResumeOut)
# async def create_resume(resume: schemas.ResumeCreate, current_user: User = Depends(get_current_user)):
#     async with async_session() as session:
#         return await service.create_resume(session, resume, current_user.id)

# @router.get("/{resume_id}", response_model=schemas.ResumeOut)
# async def read_resume(resume_id: int, current_user: User = Depends(get_current_user)):
#     async with async_session() as session:
#         resume = await service.get_resume(session, resume_id, current_user.id)
#         if not resume:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
#         return resume

# @router.get("/", response_model=list[schemas.ResumeOut])
# async def read_resumes(current_user: User = Depends(get_current_user)):
#     async with async_session() as session:
#         return await service.get_resumes(session, current_user.id)

# @router.put("/{resume_id}", response_model=schemas.ResumeOut)
# async def update_resume(resume_id: int, resume: schemas.ResumeUpdate, current_user: User = Depends(get_current_user)):
#     async with async_session() as session:
#         updated_resume = await service.update_resume(session, resume_id, current_user.id, resume)
#         if not updated_resume:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
#         return updated_resume

# @router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_resume(resume_id: int, current_user: User = Depends(get_current_user)):
#     async with async_session() as session:
#         success = await service.delete_resume(session, resume_id, current_user.id)
#         if not success:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

# @router.post("/generate-pdf")
# async def generate_pdf(data: schemas.ResumeData):
#     # print("Data", data.model_dump())
#     result = await service.generate_resume_pdf(data.model_dump())

#     if isinstance(result, FileResponse):
#         return result
#     return JSONResponse(status_code=500, content=result)

import time

import time
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, JSONResponse

router = APIRouter()

@router.post("/generate-pdf")
async def generate_pdf(request: Request):
    start_time = time.time()  # Use time.time() for total elapsed time

    data = await request.json()
    result = await service.generate_resume_pdf(data)

    end_time = time.time()
    process_time = end_time - start_time
    print(f"PDF generation process time: {process_time:.4f} seconds")

    if isinstance(result, FileResponse):
        return result
    return JSONResponse(status_code=500, content=result)
