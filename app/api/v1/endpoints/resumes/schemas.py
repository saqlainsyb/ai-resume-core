from pydantic import BaseModel
from datetime import datetime

class ResumeBase(BaseModel):
    title: str
    template_id: int

class ResumeCreate(ResumeBase):
    pass

class ResumeUpdate(BaseModel):
    title: str | None = None
    template_id: int | None = None

class ResumeOut(ResumeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
