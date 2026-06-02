"""create posts table

Revision ID: 823d90f75d6d
Revises: 
Create Date: 2026-06-01 23:00:22.514375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '823d90f75d6d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True), sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
