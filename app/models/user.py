from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime, func

from app.database import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'tracker'}

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
