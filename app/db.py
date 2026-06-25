from typing import Annoted

from fastapi.params import Depends
from sqlmodel import Session, create_engine

sqlite_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annoted[Session, Depends(get_session)]
