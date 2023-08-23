"""create user table

Revision ID: 5e9e8266f640
Revises: 
Create Date: 2023-08-23 14:01:15.780576

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e9e8266f640'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('name', sa.VARCHAR(50), nullable=False),
        sa.Column('description', sa.VARCHAR(255)),
    )

def downgrade():
    op.drop_table('account')