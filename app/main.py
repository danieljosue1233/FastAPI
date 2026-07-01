import time
import zoneinfo
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated

from db import create_all_tables
from models import Invoice

from .routers import customers, plans, transactions

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} completed in: {process_time:.4f}seconds")
    return response


security = HTTPBasic()


@app.get("/")
async def root(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    print(credentials)
    if credentials.username != "admin" or credentials.password != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"message": f"Welcome back, {credentials.username}!"}


country_timezones = {
    "US": "America/New_York",
    "GB": "Europe/London",
    "IN": "Asia/Kolkata",
    "JP": "Asia/Tokyo",
}


@app.get("/time/{iso_code}")
async def get_time_by_iso_code(iso_code: str):
    iso = iso_code = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str) if timezone_str else zoneinfo.ZoneInfo("UTC")
    return {"time": datetime.now(tz).isoformat(), "iso_code": iso_code}


# db_customers: list[Customer] = []


@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data
