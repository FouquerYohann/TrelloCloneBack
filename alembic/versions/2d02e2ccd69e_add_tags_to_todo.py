"""Add tags to Todo

Revision ID: 2d02e2ccd69e
Revises: a81124616abf
Create Date: 2023-08-10 10:44:26.469035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ARRAY, String

from sql_app.models.tags import TAG_TABLE_NAME
from sql_app.models.todo import TODO_TABLE_NAME
from sql_app.models.todo_tag_association import TODO_TAG_TABLE_NAME

# revision identifiers, used by Alembic.
revision: str = '2d02e2ccd69e'
down_revision: Union[str, None] = 'a81124616abf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(TAG_TABLE_NAME,
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("name", sa.String(10), nullable=False, unique=True))
    op.create_table(TODO_TAG_TABLE_NAME,
                    sa.Column("todo_id", sa.Integer, sa.ForeignKey("todos.id")),
                    sa.Column("tag_id", sa.Integer, sa.ForeignKey("tags.id")))


def downgrade() -> None:
    op.drop_table(TODO_TAG_TABLE_NAME)
    op.drop_table(TAG_TABLE_NAME)
