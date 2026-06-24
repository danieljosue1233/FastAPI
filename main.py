import zoneinfo
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    description: str | None
    email: str
    age: int


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


app.post("/customers")
async def create_customer(customer_data: Customer):
    return customer_data
