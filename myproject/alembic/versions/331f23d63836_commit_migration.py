"""Commit migration

Revision ID: 331f23d63836
Revises: 46fa6e3a2b42
Create Date: 2023-08-29 11:59:54.758411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '331f23d63836'
down_revision: Union[str, None] = '46fa6e3a2b42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('systeminfo', sa.Column('gpu_id', sa.Float(), nullable=True))
    op.add_column('systeminfo', sa.Column('gpu_name', sa.String(), nullable=True))
    op.add_column('systeminfo', sa.Column('gpu_memory_total', sa.Float(), nullable=True))
    op.add_column('systeminfo', sa.Column('gpu_memory_free', sa.Float(), nullable=True))
    op.add_column('systeminfo', sa.Column('gpu_memory_used', sa.Float(), nullable=True))
    op.add_column('systeminfo', sa.Column('gpu_utilization', sa.Float(), nullable=True))
    op.drop_column('systeminfo', 'gpu_info')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('systeminfo', sa.Column('gpu_info', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('systeminfo', 'gpu_utilization')
    op.drop_column('systeminfo', 'gpu_memory_used')
    op.drop_column('systeminfo', 'gpu_memory_free')
    op.drop_column('systeminfo', 'gpu_memory_total')
    op.drop_column('systeminfo', 'gpu_name')
    op.drop_column('systeminfo', 'gpu_id')
    # ### end Alembic commands ###