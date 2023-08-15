"""Adding avatar path to people table

Revision ID: 31030e9bb2cd
Revises: 2d02e2ccd69e
Create Date: 2023-08-14 12:24:22.960780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sql_app.models.people import PEOPLE_TABLE_NAME

# revision identifiers, used by Alembic.
revision: str = '31030e9bb2cd'
down_revision: Union[str, None] = '2d02e2ccd69e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(PEOPLE_TABLE_NAME, sa.Column("avatar_path", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column(PEOPLE_TABLE_NAME, "avatar_path")
