import zoneinfo
from datetime import datetime

from db import SessionDep
from fastapi import FastAPI

from .models import Customer, CustomerCreate, Invoice, Transaction

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


country_timezones = {
    "US": "America/New_York",
    "GB": "Europe/London",
    "IN": "Asia/Kolkata",
    "JP": "Asia/Tokyo",
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str) if timezone_str else zoneinfo.ZoneInfo("UTC")
    return {"time": datetime.now(tz).isoformat(), "iso_code": iso_code}


db_customers: list[Customer] = []


@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session=SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    # Asumiendo que hace base de datos, se incrementa el ID del cliente
    customer.id = len(db_customers)
    db_customers.append(customer)
    return customer


@app.get("/customers", response_model=list[Customer])
async def list_customers():
    return db_customers


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data
