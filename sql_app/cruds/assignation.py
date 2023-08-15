from sqlalchemy.orm import Session

from sql_app.cruds.people import get_people_by_id
from sql_app.cruds.todo import crud_get_todo_by_id


def assign_task(db: Session, people_id: int, task_id: int):
    people = get_people_by_id(db, people_id)
    task = crud_get_todo_by_id(db, task_id)

    if people is None or task is None:
        return False

    people.assigned.append(task)
    db.commit()
