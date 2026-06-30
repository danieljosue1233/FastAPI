from math import ceil

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import func, select

from db import SessionDep
from models import Customer, Transaction, TransactionCreate

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    session: SessionDep,
):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict["customer_id"])
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    transaction_db = Transaction.model_validate(transaction_data_dict)

    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db


# @router.get("/")
# async def list_transactions(session: SessionDep):
#     query = select(Transaction)
#     transactions = session.exec(query).all()
#     print(f"Cantidad de transacciones: {len(transactions)}")
#     return transactions


@router.get("/")
async def list_transactions(
    session: SessionDep,
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, ge=1, description="Número de registros"),
):

    total_items = session.exec(select(func.count()).select_from(Transaction)).one()

    transactions = session.exec(select(Transaction).offset(skip).limit(limit)).all()

    total_pages = ceil(total_items / limit) if total_items > 0 else 0

    return {
        "data": transactions,
        "pagination": {
            "total_items": total_items,
            "total_pages": total_pages,
            "items_on_page": len(transactions),
            "per_page": limit,
            "current_page": (skip // limit) + 1,
        },
    }
