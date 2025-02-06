from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi import Depends

DATABASE_URL = "postgresql://postgres:Qazwsx12@db:5432/test"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
