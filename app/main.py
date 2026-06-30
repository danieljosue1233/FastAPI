import zoneinfo
from datetime import datetime

from fastapi import FastAPI

from db import create_all_tables
from models import Invoice

from .routers import customers, plans, transactions

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)


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


# db_customers: list[Customer] = []


@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data
