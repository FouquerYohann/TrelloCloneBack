from fastapi import HTTPException
from sqlalchemy.orm import Session

from sql_app.models.people import People
from sql_app.models.tags import Tag
from sql_app.models.todo import Todo
from sql_app.schemas.todo import PyTodoIn


def crud_get_todo_by_id(db: Session, todo_id: int) -> Todo | None:
    return db.query(Todo).filter(Todo.id == todo_id).first()


def crud_get_todo_by_title(db: Session, title: str):
    return db.query(Todo).filter(Todo.title.like(f"%{title}%")).first()


def crud_get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).offset(skip).limit(limit)


def crud_delete_todo(db: Session, todo_id: int):
    db_todo = crud_get_todo_by_id(db, todo_id)
    db.delete(db_todo)
    db.commit()
    return True


def crud_patch_todo_by_id(db: Session, todo_id: int, todo: PyTodoIn):
    db_task: Todo = crud_get_todo_by_id(db, todo_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # TODO get dictionnary from db_task and update to values from pythodoin
    db_task.status = todo.status
    db_task.description = todo.description
    db_task.title = todo.title

    # TODO wonder if importing crud will give circular dependencies
    assignee = db.query(People).filter(People.id == todo.assignee_id).first()
    if assignee is not None:
        db_task.assignee_id = todo.assignee_id

    db_tags = get_or_create_tags(db, todo.tags)
    db_task.tags = db_tags

    db.commit()
    return db_task


def crud_create_todo(db: Session, todo: PyTodoIn):

    dump = todo.model_dump()
    tags = dump.pop("tags")
    db_todo = Todo(**dump)

    db_tags = get_or_create_tags(db, tags)

    db_todo.tags = db_tags

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_or_create_tags(db: Session, tags: list[str]):
    db_tags = []
    for tag_name in tags:
        db_tag = db.query(Tag).filter(Tag.name == tag_name).first()

        if db_tag is None:
            db_tag = Tag(name=tag_name)
            db.add(db_tag)

        db_tags.append(db_tag)

    return db_tags
