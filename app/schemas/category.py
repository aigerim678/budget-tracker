from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str | None = None
    user_id: int


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int
