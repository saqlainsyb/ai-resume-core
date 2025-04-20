from pydantic import BaseModel
from datetime import datetime

class TemplateBase(BaseModel):
    name: str

class TemplateOut(TemplateBase):
    id: int
    created_at: datetime
    preview_image: str 

    class Config:
        orm_mode = True
