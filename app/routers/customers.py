from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db import SessionDep
from models import Customer, CustomerCreate, CustomerUpdate

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    # Asumiendo que hace base de datos, se incrementa el ID del cliente
    # customer.id = len(db_customers)
    # db_customers.append(customer)
    return customer


@router.get("/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer_db


@router.patch(
    "/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
)
async def update_customer(
    customer_id: int, customer_data: CustomerUpdate, session: SessionDep
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db


@router.delete("/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}


@router.get("/", response_model=list[Customer])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()
