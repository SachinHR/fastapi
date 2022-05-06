"""Add last few columns to posts table

Revision ID: 64a2111ea7fd
Revises: 3a637d68a2f7
Create Date: 2022-05-06 17:50:49.610885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64a2111ea7fd'
down_revision = '3a637d68a2f7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()") ,nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "Published")
    op.drop_column("posts", "created_at")
    pass
