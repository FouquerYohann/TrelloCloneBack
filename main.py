import shutil

from fastapi import FastAPI, Depends, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import File
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from sql_app.cruds.assignation import assign_task
from sql_app.cruds.people import get_people, create_people, crud_updload_avatar, get_people_by_id
from sql_app.cruds.tags import crud_get_tags, crud_create_tag
from sql_app.cruds.todo import crud_create_todo, crud_get_todos, crud_patch_todo_by_id, crud_delete_todo
from sql_app.database import Base, engine, SessionLocal
from sql_app.schemas.people import PyPeopleIn, PyPeopleOut
from sql_app.schemas.tags import PyTagOut, PyTagIn
from sql_app.schemas.todo import PyTodoIn, PyTodoOut

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/todos", response_model=PyTodoOut)
def post_todo(todo: PyTodoIn, db: Session = Depends(get_db)):
    return crud_create_todo(db, todo)


@app.get("/todos", response_model=list[PyTodoOut])
def read_todo(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_get_todos(db, skip, limit)


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id : int, db: Session = Depends(get_db)):
    return crud_delete_todo(db, todo_id)


@app.patch("/todos/{todo_id}/patch", response_model=PyTodoOut)
def change_status(todo_id: int, task: PyTodoIn, db: Session = Depends(get_db)):
    return crud_patch_todo_by_id(db, todo_id, task)


@app.post("/people", response_model=PyPeopleOut)
def post_people(people: PyPeopleIn, db: Session = Depends(get_db)):
    return create_people(db, people)


@app.put("/people/{people_id}/avatar", response_model=PyPeopleOut)
def put_people_avatar(people_id: int, avatar_img: UploadFile = File(), db: Session = Depends(get_db)):
    avatar_location = f"people_avatar/{people_id}_{avatar_img.filename}"
    with open(avatar_location, "wb+") as file_object:
        shutil.copyfileobj(avatar_img.file, file_object)

    return crud_updload_avatar(db, people_id, avatar_location)


@app.get("/people/{people_id}/avatar")
def get_people_avatar(people_id: int, db: Session = Depends(get_db)):
    db_person = get_people_by_id(db, people_id)
    if db_person is not None:
        truc = db_person.avatar_path.replace("/", "\\")
        truc2 = f'C:\\Users\\Yohann Fouquer\\PycharmProjects\\fastApiProject\\{truc}'
        return FileResponse(truc2)
    else:
        raise HTTPException(404)


@app.get("/people", response_model=list[PyPeopleOut])
def read_people(db: Session = Depends(get_db)):
    return get_people(db)


@app.get("/assign/{people_id}/{task_id}")
def assign_people_task(people_id: int, task_id: int, db: Session = Depends(get_db)):
    return assign_task(db, people_id, task_id)


@app.post("/tags", response_model=PyTagOut)
def create_tag(tag_in: PyTagIn, db=Depends(get_db)):
    return crud_create_tag(db, tag_in)


@app.get("/tags", response_model=list[PyTagOut])
def read_tags(limit: int = 100, offset: int = 0, db=Depends(get_db)):
    return crud_get_tags(db, limit, offset)
