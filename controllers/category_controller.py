from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, update,delete
from models.category import Categories
from database import SessionDep
from typing import Optional
from controllers.user_controller import get_current_user
from models.users import Users
from pydantic import BaseModel

router = APIRouter()

@router.get("/categories/{category_id}")
def get_category(category_id: int, session: SessionDep, current_user: Users = Depends(get_current_user)):
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

@router.post("/categories/")
def add_category(name: str, parent_id: Optional[int] = None, session: SessionDep = SessionDep, current_user: Users = Depends(get_current_user)):
    parent = None
    if parent_id:
        parent = session.get(Categories, parent_id)
        if not parent:
            raise HTTPException(status_code=404, detail="Родительская категория не найдена")

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

@router.delete("/categories/{category_id}")
def delete_category(category_id: int, session: SessionDep, current_user: Users = Depends(get_current_user)):
    category = session.get(Categories, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    lft, rgt = category.lft, category.rgt
    width = rgt - lft + 1

    session.exec(
        delete(Categories).where(Categories.lft.between(lft, rgt))
    )

    session.exec(
        update(Categories)
        .where(Categories.rgt > rgt)
        .values(rgt=Categories.rgt - width)
    )

    session.exec(
        update(Categories)
        .where(Categories.lft > rgt)
        .values(lft=Categories.lft - width)
    )

    session.commit()

    return {"message": "Категория удалена.", "id":category_id}


@router.put("/categories/{category_id}")
def update_category(category_id: int, name: str, session: SessionDep, current_user: Users = Depends(get_current_user)):
    category = session.get(Categories, category_id)
    if not category:

        raise HTTPException(status_code=404, detail="Категория не найдена")

    category.name = name
    session.add(category)
    session.commit()

    return {"message": "Название категории обновлено.", "id": category.id, "new_name": category.name}