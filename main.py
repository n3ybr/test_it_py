from sqlmodel import SQLModel, Field, create_engine, Session, select, update
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, List, Optional
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:Qazwsx12@localhost:5432/test"

engine = create_engine(DATABASE_URL)

class Categories(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    parent_id: Optional[int] = Field(default=None)
    lft: int
    rgt: int

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.get("/categories/{category_id}", response_model=List[Categories])
def get_category(category_id: int, session: SessionDep):
    category = session.get(Categories, category_id)

    if not category:

        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    query = (
        select(Categories)
        .where(Categories.lft > category.lft, Categories.rgt < category.rgt)
        .order_by(Categories.lft)
    )   

    categories = session.exec(query).all()

    return categories

@app.post("/categories/")
def add_category(name: str, parent_id: Optional[int] = None, session: SessionDep = SessionDep):
    parent = None
    if parent_id:
        parent = session.get(Categories, parent_id)
        if not parent:
            raise HTTPException(status_code=404, detail="Родительская категория не найдена.")

    if not parent:
        max_rgt = session.exec(select(Categories.rgt).order_by(Categories.rgt.desc())).first()
        lft = (max_rgt + 1) if max_rgt else 1
        rgt = lft + 1
    else:
        session.exec(
            update(Categories)
            .where(Categories.rgt >= parent.rgt)
            .values(rgt=Categories.rgt + 2)
        )

        session.exec(
            update(Categories)
            .where(Categories.lft > parent.rgt)
            .values(lft=Categories.lft + 2)
        )

        lft = parent.rgt
        rgt = parent.rgt + 1

        session.exec(
            update(Categories)
            .where(Categories.id == parent.id)
            .values(rgt=parent.rgt + 2)
        )

    new_category = Categories(name=name, parent_id=parent_id, lft=lft, rgt=rgt)
    session.add(new_category)
    session.commit()

    return {"message": f"Категория '{name}' добавлена.", "id": new_category.id}













