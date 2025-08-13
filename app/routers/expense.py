import asyncio
import json
from typing import List, Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ExpenseOut, ExpenseCreate, UserOut
from app.repository import get_all_expenses, get_expense_by_id, add_expense, get_my_expenses
from app.dependencies import get_current_user
from app.clients import redis_client

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


@router.get("/{id}", response_model=ExpenseOut)
async def read_expense(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    cached_expense = redis_client.get(f"expense_{id}")

    if cached_expense:
        expense_dict = json.loads(cached_expense)
        return ExpenseOut(**expense_dict)

    await asyncio.sleep(2)

    expense = await get_expense_by_id(expense_id=id, session=db)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    redis_client.set(f"expense_{id}", json.dumps(jsonable_encoder(expense)))
    return expense


@router.post("/", response_model=ExpenseOut)
async def create_expense(expense: ExpenseCreate,
                         current_user: Annotated[UserOut, Depends(get_current_user)],
                         db: Annotated[AsyncSession, Depends(get_db)]):
    return await add_expense(expense=expense, user_id=current_user.id, session=db)
