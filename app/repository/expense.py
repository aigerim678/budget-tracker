from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Category, Expense
from app.schemas import ExpenseCreate


async def get_all_expenses(session: AsyncSession) -> List[Expense]:
    result = await session.execute(
        select(Expense)
    )
    return result.scalars().all()


async def get_expense_by_id(expense_id: int, session: AsyncSession) -> Expense:
    result = await session.execute(
        select(Expense).where(Expense.id == expense_id)
    )

    return result.scalars().first()


async def get_my_expenses(user_id: int, category_name: str, session: AsyncSession) -> List[Expense]:
    query = select(Expense).where(Expense.user_id == user_id)

    if category_name:
        category_obj = await session.execute(
            select(Category).where(
                Category.name == category_name,
                Category.user_id == user_id
            )
        )
        category_obj = category_obj.scalar_one_or_none()

        if category_obj is None:
            raise HTTPException(status_code=400, detail="Category not found or not yours")

        query = query.where(Expense.category_id == category_obj.id)

    result = await session.execute(query)

    return result.scalars().all()


async def get_my_expenses_by_category(user_id: int, session: AsyncSession) -> List[Expense]:
    result = await session.execute(
        select(Expense).where(Expense.user_id == user_id)
    )

    return result.scalars().all()


async def add_expense(expense: ExpenseCreate, user_id: int, session: AsyncSession) -> Expense:
    category = await session.execute(
        select(Category).where(
            Category.name == expense.category,
            Category.user_id == user_id
        )
    )
    category = category.scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=400, detail="Category not found or not yours")

    new_expense = Expense(
        amount=expense.amount,
        currency=expense.currency,
        date=expense.date,
        description=expense.description,
        user_id=user_id,
        category_id=category.id,
    )
    session.add(new_expense)

    await session.commit()
    await session.refresh(new_expense)
    return new_expense
