"""add content column to posts tabel

Revision ID: f0edfa1bb025
Revises: 823d90f75d6d
Create Date: 2026-06-01 23:19:46.255455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0edfa1bb025'
down_revision = '823d90f75d6d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
