from sqlmodel import Session, select
from main import Categories, engine

def calculate_nested_set(session: Session):
    counter = 1 

    def process_node(category_id, counter):
        category = session.get(Categories, category_id)
        category.lft = counter
        counter += 1

        children = session.exec(
            select(Categories).where(Categories.parent_id == category_id).order_by(Categories.id)
        ).all()

        for child in children:
            counter = process_node(child.id, counter) 

        category.rgt = counter
        counter += 1

        session.add(category)
        session.commit()

        return counter

    root_categories = session.exec(
        select(Categories).where(Categories.parent_id == None)
    ).all()

    for root in root_categories:
        counter = process_node(root.id, counter)

with Session(engine) as session:
    calculate_nested_set(session)
