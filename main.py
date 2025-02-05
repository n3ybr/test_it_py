from sqlmodel import SQLModel, Field, create_engine, Session, select
from fastapi import FastAPI, Depends
from typing import Annotated, List, Optional

DATABASE_URL = "postgresql://postgres:Qazwsx12@localhost:5432/test"

engine = create_engine(DATABASE_URL)

class Categories(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    parent_id: Optional[int] = Field(default=None)
    path: str

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.get("/categories/{category_id}", response_model=List[Categories])
def get_category(category_id: int, session: SessionDep):
    query = select(Categories).where(Categories.path.contains(str(category_id))).order_by(Categories.path)
    categories = session.exec(query).all()
    return categories[1:]
