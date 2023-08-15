from typing import List, TYPE_CHECKING, Set

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sql_app.database import Base
from sql_app.models.todo_tag_association import todo_tag_association_table


if TYPE_CHECKING:
    from sql_app.models.todo import Todo


TAG_TABLE_NAME = "tags"


class Tag(Base):
    __tablename__ = TAG_TABLE_NAME

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    todos: Mapped[List["Todo"]] = relationship(secondary=todo_tag_association_table, back_populates="tags")

