"""add column published, created_at to posts table

Revision ID: f3627417e5f7
Revises: 20ebd2e7cfe4
Create Date: 2026-06-02 05:30:29.256613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3627417e5f7'
down_revision = '20ebd2e7cfe4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default='True'))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
