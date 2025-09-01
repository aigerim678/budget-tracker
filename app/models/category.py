from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Text, Integer, ForeignKey, UniqueConstraint

from app.database import Base
from app.settings import database


class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = (UniqueConstraint('user_id', 'name', name='uq_category_name_user'),
                      {'schema': database.schema})

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('tracker.users.id'), nullable=False)
