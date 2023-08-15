from typing import Set

from pydantic import BaseModel


class PyTagBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class PyTagIn(PyTagBase):
    pass


class PyTagOutMinimal(PyTagBase):
    id: int


class PyTagOut(PyTagOutMinimal):
    todos: list["PyTodoOutMinimal"]


from sql_app.schemas.todo import PyTodoOutMinimal
PyTagOut.model_rebuild()
