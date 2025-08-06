from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import Category
from app.schemas import CategoryCreate


async def get_all_categories(session: AsyncSession) -> List[Category]:
    result = await session.execute(
        select(Category)
    )
    return result.scalars().all()


async def get_category_by_id(category_id: int, session: AsyncSession) -> Category:
    result = await session.execute(
        select(Category).where(Category.id == category_id)
    )

    return result.scalars().first()


async def get_my_categories(user_id: int, session: AsyncSession) -> List[Category]:
    result = await session.execute(
        select(Category).where(Category.user_id == user_id)
    )

    return result.scalars().all()


async def add_category(category: CategoryCreate, user_id: int, session: AsyncSession) -> Category:
    new_category = Category(
        name=category.name,
        description=category.description,
        user_id=user_id,
    )
    session.add(new_category)
    try:
        await session.commit()
        await session.refresh(new_category)
        return new_category
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this user already exists.",
        )
