from enum import Enum as PythonEnum
from sqlalchemy import Enum, ARRAY
from typing import Optional, Type, TYPE_CHECKING, List, Set

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sql_app.database import Base
from sql_app.models.todo_tag_association import todo_tag_association_table

if TYPE_CHECKING:
    from sql_app.models.people import People
    from sql_app.models.tags import Tag


class TodoStatus(str, PythonEnum):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'


TODO_TABLE_NAME = "todos"


class Todo(Base):
    __tablename__ = TODO_TABLE_NAME

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]]
    status: Mapped[TodoStatus] = mapped_column(Enum(TodoStatus))
    assignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("people.id"))

    tags: Mapped[List["Tag"]] = relationship(secondary=todo_tag_association_table, back_populates="todos")
    assignee: Mapped["People"] = relationship(back_populates="assigned")

    def __repr__(self) -> str:
        return f"Todo(id={self.tid}, title={self.title}, description={self.description}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
