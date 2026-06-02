"""add users table

Revision ID: 0b7aa3dfe858
Revises: f0edfa1bb025
Create Date: 2026-06-01 23:39:54.951012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b7aa3dfe858'
down_revision = 'f0edfa1bb025'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"))
    pass


def downgrade():
    op.drop_table("users")
    pass
