from fastapi import APIRouter
from sqlmodel import select, update
from models.category import Categories
from database import SessionDep
from typing import Optional

router = APIRouter()

@router.get("/categories/{category_id}")
def get_category(category_id: int, session: SessionDep):
    category = session.get(Categories, category_id)

    if not category:
        return {"error": "Категория не найдена"}, 404
        
    query = (
        select(Categories)
        .where(Categories.lft > category.lft, Categories.rgt < category.rgt)
        .order_by(Categories.lft)
    )   

    categories = session.exec(query).all()
    return categories

@router.post("/categories/")
def add_category(name: str, parent_id: Optional[int] = None, session: SessionDep = SessionDep):
    parent = None
    if parent_id:
        parent = session.get(Categories, parent_id)
        if not parent:
            return {"error": "Родительская категория не найдена"}, 404

    if not parent:
        max_rgt = session.exec(select(Categories.rgt).order_by(Categories.rgt.desc())).first()
        lft = (max_rgt + 1) if max_rgt else 1
        rgt = lft + 1
    else:
        session.exec(update(Categories).where(Categories.rgt >= parent.rgt).values(rgt=Categories.rgt + 2))
        session.exec(update(Categories).where(Categories.lft > parent.rgt).values(lft=Categories.lft + 2))

        lft = parent.rgt
        rgt = parent.rgt + 1

        session.exec(update(Categories).where(Categories.id == parent.id).values(rgt=parent.rgt + 2))

    new_category = Categories(name=name, parent_id=parent_id, lft=lft, rgt=rgt)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return {"message": f"Категория '{name}' добавлена.", "id": new_category.id}
