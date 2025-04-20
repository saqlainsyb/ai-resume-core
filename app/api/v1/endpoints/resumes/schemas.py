from pydantic import BaseModel
from datetime import datetime

class ResumeBase(BaseModel):
    title: str
    template_id: int

from pydantic import BaseModel
from typing import List

class ExperienceIn(BaseModel):
    company: str
    role: str
    start: str
    end: str
    details: str
    current: bool

class EducationIn(BaseModel):
    institution: str
    degree: str
    start: str
    end: str

class ResumeCreate(ResumeBase):
    firstName: str
    lastName:  str
    email:     str
    phone:     str
    summary:   str
    experiences: List[ExperienceIn]
    education:   List[EducationIn]
    skills:      List[str]

    model_config = {
      "extra": "ignore"   # or "forbid", if you want to catch typos
    }
    

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
