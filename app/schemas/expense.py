from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class CurrencyEnum(str, Enum):
    USD = "USD"
    KZT = "KZT"
    RUB = "RUB"


class ExpenseBase(BaseModel):
    amount: float
    currency: CurrencyEnum = CurrencyEnum.KZT
    description: str | None = None
    date: date


class ExpenseCreate(ExpenseBase):
    category: str


class ExpenseOut(ExpenseBase):
    id: int
    user_id: int
    category_id: int
