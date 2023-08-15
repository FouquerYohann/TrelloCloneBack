"""Alter Todo table to add status

Revision ID: a81124616abf
Revises: 
Create Date: 2023-08-09 12:24:16.650736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sql_app.models.todo import TODO_TABLE_NAME, TodoStatus

# revision identifiers, used by Alembic.
revision: str = 'a81124616abf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(TODO_TABLE_NAME, sa.Column("status", sa.Enum(TodoStatus)))
    op.execute(f"UPDATE {TODO_TABLE_NAME} SET status = '{TodoStatus.TODO.name}' WHERE status IS NULL ")


def downgrade() -> None:
    op.drop_column(TODO_TABLE_NAME, "status")
