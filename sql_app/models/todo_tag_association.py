from sqlalchemy import Table, Column, Integer, ForeignKey

from sql_app.database import Base

TODO_TAG_TABLE_NAME = "todo_tag"

todo_tag_association_table = Table(
    TODO_TAG_TABLE_NAME,
    Base.metadata,
    Column("todo_id", Integer, ForeignKey("todos.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)
