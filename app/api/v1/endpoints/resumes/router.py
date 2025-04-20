from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.api.v1.endpoints.resumes import schemas, service
from app.api.v1.endpoints.auth.utils import get_current_user
from app.api.v1.endpoints.auth.models import User
from app.core.templates import templates

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

@router.post(
    "/preview",
    response_class=HTMLResponse,
    tags=["Preview"],
)
async def preview_resume(
    data: schemas.ResumeCreate,
    request: Request
):
    """
    Render a live‑preview of the resume data without saving to DB.
    """
    # 1) Dump all the fields from the Pydantic model
    raw = data.model_dump()

    # 2) Build a `user` dict exactly matching what template01.jinja2 uses:
    user_ctx = {
        # combine first and last name
        "name": f"{raw.get('firstName','')} {raw.get('lastName','')}".strip(),
        # your form’s `title` field is actually the user’s job title
        "title": raw.get("title", ""),
        # placeholder for photo; your form doesn’t send this yet
        "photo_base64": None,
        # basic contact & profile
        "summary": raw.get("summary", ""),
        "phone":   raw.get("phone", ""),
        "email":   raw.get("email", ""),
        # if you collect these in the form, add them; otherwise leave blank
        "location": raw.get("location", ""),
        "linkedin": raw.get("linkedin", ""),
        # skills array
        "skills": raw.get("skills", []),
        # Jinja loops over `user.experience`, so rename `experiences` → `experience`
        "experience": raw.get("experiences", []),
        # Jinja expects edu items to have `gpa`; if you don’t collect it, supply empty string
        "education": [
            {
              **edu,
              "gpa": edu.get("gpa","")
            }
            for edu in raw.get("education", [])
        ]
    }

    # 3) Pass that under "user" so your existing template01.jinja2 works unmodified :contentReference[oaicite:0]{index=0}&#8203;:contentReference[oaicite:1]{index=1}
    context = {
      "request": request,
      "user":    user_ctx
    }

    template_name = f"template0{data.template_id}.jinja2"
    return templates.TemplateResponse(template_name, context)
