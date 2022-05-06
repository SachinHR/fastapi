"""Add content column to post table

Revision ID: ba7371ccd216
Revises: c63013cc869a
Create Date: 2022-05-06 17:16:53.679606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba7371ccd216'
down_revision = 'c63013cc869a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
