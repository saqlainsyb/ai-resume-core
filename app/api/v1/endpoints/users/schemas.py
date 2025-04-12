from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
