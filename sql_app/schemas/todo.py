from typing import Optional, List, TYPE_CHECKING, Set

from pydantic import BaseModel

from sql_app.models.todo import TodoStatus


class PyTodoBase(BaseModel):
    title: str
    description: str | None = None
    status: TodoStatus | None = TodoStatus.TODO

    class Config:
        from_attributes = True


class PyTodoIn(PyTodoBase):
    assignee_id: int | None = None
    tags: List[str]


class PyTodoOutMinimal(PyTodoBase):
    id: int
    assignee_id: int | None = None


class PyTodoOut(PyTodoOutMinimal):
    assignee: Optional["PyPeopleOutMinimal"]
    tags: list["PyTagOutMinimal"]


from sql_app.schemas.people import PyPeopleOutMinimal
from sql_app.schemas.tags import PyTagOutMinimal
PyTodoOut.model_rebuild()
