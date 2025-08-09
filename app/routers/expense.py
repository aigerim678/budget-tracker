from typing import List, Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ExpenseOut, ExpenseCreate, UserOut
from app.repository import get_all_expenses, get_expense_by_id, add_expense, get_my_expenses
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}}
)


@router.get("/all-users", response_model=List[ExpenseOut], description="For admins")
async def read_all_expenses(current_user: Annotated[UserOut, Depends(get_current_user)],
                            db: Annotated[AsyncSession, Depends(get_db)]):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await get_all_expenses(session=db)


@router.get("/", response_model=List[ExpenseOut])
async def read_my_expenses(
        current_user: Annotated[UserOut, Depends(get_current_user)],
        db: Annotated[AsyncSession, Depends(get_db)],
        category: str | None = None, ):
    return await get_my_expenses(user_id=current_user.id, category_name=category, session=db)


@router.get("/{id}", response_model=ExpenseOut)
async def read_expense(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_expense_by_id(expense_id=id, session=db)


@router.post("/", response_model=ExpenseOut)
async def create_expense(expense: ExpenseCreate,
                         current_user: Annotated[UserOut, Depends(get_current_user)],
                         db: Annotated[AsyncSession, Depends(get_db)]):
    return await add_expense(expense=expense, user_id=current_user.id, session=db)
