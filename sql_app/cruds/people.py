import os

from sqlalchemy.orm import Session

from sql_app.models.people import People
from sql_app.models.todo import Todo
from sql_app.schemas.people import PyPeopleIn, PyPeopleBase


def get_people(db: Session):
    return db.query(People).all()


def get_people_by_name(db: Session, search: str):
    return db.query(People).filter(People.first_name.like(f"%{search}%") | People.last_name.like(f"%{search}%")).all()


def get_people_by_id(db: Session, people_id: int) -> People | None:
    return db.query(People).filter(People.id == people_id).first()


def crud_updload_avatar(db: Session, people_id: int, avatar_path: str):
    db_person = db.query(People).where(People.id == people_id).first()

    if db_person.avatar_path is not None and db_person.avatar_path != avatar_path:
        print("NOT NONE HERE")
        print("db_person.avatar_path")
        truc = db_person.avatar_path.replace("/", "\\")
        os.remove(f'C:\\Users\\Yohann Fouquer\\PycharmProjects\\fastApiProject\\{truc}')

    db_person.avatar_path = avatar_path
    db.commit()
    db.refresh(db_person)
    return db_person


def create_people(db: Session, people: PyPeopleIn):
    dump = people.model_dump()
    assigned_ids = dump.pop("assigned_ids")

    db_people = People(**dump)
    db.add(db_people)
    db.commit()
    db.refresh(db_people)

    for assigned_id in assigned_ids:
        todo_task = db.query(Todo).where(Todo.id == assigned_id).first()
        if todo_task is not None:
            db_people.assigned.append(todo_task)

    db.commit()
    return db_people
