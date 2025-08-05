from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime, Text, Integer, ForeignKey, Numeric

from app.database import Base


class Expense(Base):
    __tablename__ = 'expenses'
    __table_args__ = {'schema': 'tracker'}

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default='KZT')
    description: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
