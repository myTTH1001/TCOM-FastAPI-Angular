"""Commit migration

Revision ID: 65e1c83089b8
Revises: 4cd08faf0b84
Create Date: 2023-08-24 11:37:09.039627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65e1c83089b8'
down_revision: Union[str, None] = '4cd08faf0b84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_blog')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_blog',
    sa.Column('blog_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['blog_id'], ['blog.id'], name='user_blog_blog_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_blog_user_id_fkey')
    )
    # ### end Alembic commands ###
