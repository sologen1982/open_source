"""Roles

Revision ID: 5404286ccba6
Revises: fe7d433b1dcb
Create Date: 2024-06-24 21:26:27.550389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5404286ccba6'
down_revision: Union[str, None] = 'fe7d433b1dcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE TYPE role as ENUM('admin', 'moderator', 'user')")
    op.add_column('users', sa.Column('role', sa.Enum('admin', 'moderator', 'user', name='role'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    op.execute("DROP TYPE role")
    # ### end Alembic commands ###
