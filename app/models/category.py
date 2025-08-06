from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Text, Integer, ForeignKey

from app.database import Base


class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'tracker'}

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('tracker.users.id'), nullable=False)
