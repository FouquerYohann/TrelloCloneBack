from typing import List, Type

from sqlalchemy.orm import Session

from sql_app.models.tags import Tag
from sql_app.schemas.tags import PyTagIn, PyTagOut


def crud_create_tag(db: Session, tag_in: PyTagIn) -> Tag:
    db_tag = db.query(Tag).filter(Tag.name == tag_in.name).first()
    if db_tag is None:
        db_tag = Tag(**tag_in.model_dump())
        db.add(db_tag)
        db.commit()
    return db_tag


def crud_get_tags(db:Session, limit: int = 100, offset: int = 0) -> list[Type[Tag]]:
    return db.query(Tag).limit(limit).offset(offset).all()
