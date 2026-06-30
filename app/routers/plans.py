from fastapi import APIRouter
from sqlmodel import select

from db import SessionDep
from models import Plan

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post(
    "/",
)
def create_plan(plan_data: Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db


@router.get("/", response_model=list[Plan])
def list_plans(session: SessionDep):
    plans = session.exec(select(Plan)).all()
    return plans
