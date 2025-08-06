from datetime import datetime

from pydantic import BaseModel


class ExpenseBase(BaseModel):
    amount: float
    currency: str
    description: str | None = None
    date: datetime
    category_id: int


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseOut(ExpenseBase):
    id: int
    user_id: int
