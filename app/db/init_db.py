# app/db/init_db.py
import asyncio
from sqlalchemy import select, func
from app.db.base import Base
from app.db.session import engine, async_session
from app.api.v1.endpoints.templates.models import Template

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        count = await session.scalar(select(func.count()).select_from(Template))
        if count == 0:
            templates = [
                Template(name="Modern", file_path="templates/modern.html"),
                Template(name="Classic", file_path="templates/classic.html"),
            ]
            session.add_all(templates)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(init_db())
