from pydantic import BaseModel


class PyAssignation(BaseModel):
    todo_id: int
    people_id: int
