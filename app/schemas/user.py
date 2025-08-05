from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime
