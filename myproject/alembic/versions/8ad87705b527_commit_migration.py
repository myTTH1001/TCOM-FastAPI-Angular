"""Commit migration

Revision ID: 8ad87705b527
Revises: 6fdd3f4349e1
Create Date: 2023-08-28 10:37:42.219853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ad87705b527'
down_revision: Union[str, None] = '6fdd3f4349e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fileimage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fileimage_id'), 'fileimage', ['id'], unique=False)
    op.create_index(op.f('ix_fileimage_name'), 'fileimage', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_fileimage_name'), table_name='fileimage')
    op.drop_index(op.f('ix_fileimage_id'), table_name='fileimage')
    op.drop_table('fileimage')
    # ### end Alembic commands ###
