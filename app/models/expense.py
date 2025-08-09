from datetime import date

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime, Text, Integer, ForeignKey, Numeric, func

from app.database import Base
from app.settings import database


class Expense(Base):
    __tablename__ = 'expenses'
    __table_args__ = {'schema': database.schema}

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default='KZT')
    description: Mapped[str] = mapped_column(Text)
    date: Mapped[date] = mapped_column(DateTime, nullable=False, server_default=func.current_date())
    category_id: Mapped[int] = mapped_column(ForeignKey('tracker.categories.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('tracker.users.id'), nullable=False)
