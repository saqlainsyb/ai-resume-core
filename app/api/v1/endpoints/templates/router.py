from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.v1.endpoints.templates.models import Template
from app.api.v1.endpoints.templates.schemas import TemplateOut
from app.db.session import async_session

router = APIRouter()

@router.get("/", response_model=list[TemplateOut], tags=["Templates"])
async def get_templates():
    async with async_session() as session:
        result = await session.execute(select(Template))
        templates = result.scalars().all()
        if not templates:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No templates found")
        return templates
