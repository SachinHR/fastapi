"""Add user table

Revision ID: 17467d29f8f0
Revises: ba7371ccd216
Create Date: 2022-05-06 17:27:17.309418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17467d29f8f0'
down_revision = 'ba7371ccd216'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade():
    op.drop_table("users")
    pass
