from pydantic import BaseModel
from datetime import datetime

class TemplateBase(BaseModel):
    name: str
    file_path: str

class TemplateOut(TemplateBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
