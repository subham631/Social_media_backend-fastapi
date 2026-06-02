"""add owner_id foreign-key to posts

Revision ID: 20ebd2e7cfe4
Revises: 0b7aa3dfe858
Create Date: 2026-06-02 04:52:14.303952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20ebd2e7cfe4'
down_revision = '0b7aa3dfe858'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
