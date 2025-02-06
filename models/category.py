from sqlmodel import SQLModel, Field
from typing import Optional

class Categories(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    parent_id: Optional[int] = Field(default=None)
    lft: int
    rgt: int
