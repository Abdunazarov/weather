"""users table

Revision ID: 3c3d1cb7bb00
Revises: 
Create Date: 2024-02-16 16:37:37.585077

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Float



# revision identifiers, used by Alembic.
revision = '3c3d1cb7bb00'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(length=80), nullable=False),
                    sa.Column('balance', sa.Float(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username')
                    )
    
    # Define a table representation to use for the insert statement
    user_table = table('user',
                       column('username', String),
                       column('balance', Float)
                       )

    # Data to insert
    users_data = [
        {"username": "user1", "balance": 5000},
        {"username": "user2", "balance": 7500},
        {"username": "user3", "balance": 10000},
        {"username": "user4", "balance": 12500},
        {"username": "user5", "balance": 15000},
    ]

    op.bulk_insert(user_table, users_data)


def downgrade():
    op.drop_table('user')
