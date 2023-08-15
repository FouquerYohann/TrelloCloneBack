from typing import List, TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy.util import hybridproperty

from sql_app.database import Base

if TYPE_CHECKING:
    from sql_app.models.todo import Todo


PEOPLE_TABLE_NAME = "people"


class People(Base):
    __tablename__ = PEOPLE_TABLE_NAME

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(16))
    last_name: Mapped[str] = mapped_column(String(16))
    avatar_path: Mapped[Optional[str]]

    assigned: Mapped[List["Todo"]] = relationship(back_populates="assignee")

    @hybridproperty
    def avatar_url(self):
        if self.avatar_path is not None:
            return f"http://127.0.0.1:8000/people/{self.id}/avatar"
        else:
            return ""

    def __repr__(self):
        return f"People(id={self.id}), first_name={self.first_name} last_name={self.last_name}"
