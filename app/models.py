from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: str = Field(default=None)
    age: int = Field(default=None)


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class Transaction(BaseModel):
    customer_id: int
    amount: int
    description: str


class Invoice(BaseModel):
    customer_id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def total_amount(self):
        return sum(transaction.amount for transaction in self.transactions)
