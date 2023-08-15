from typing import List
from pydantic import BaseModel, Field


class PyPeopleBase(BaseModel):
    first_name: str
    last_name: str

    class Config:
        from_attributes = True



class PyPeopleIn(PyPeopleBase):
    assigned_ids: List[int] = Field(default_factory=list)


class PyPeopleOutMinimal(PyPeopleBase):
    avatar_url: str | None = None
    id: int


class PyPeopleOut(PyPeopleOutMinimal):
    assigned: "List[PyTodoOutMinimal]"


from sql_app.schemas.todo import PyTodoOutMinimal
PyPeopleOut.model_rebuild()
