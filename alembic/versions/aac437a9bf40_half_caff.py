"""half caff

Revision ID: aac437a9bf40
Revises: b2b34cb52a8d
Create Date: 2022-03-31 17:22:17.430009

"""
from alembic import op
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql as pg


# revision identifiers, used by Alembic.
revision = "aac437a9bf40"
down_revision = "b2b34cb52a8d"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("brew", Column("is_half_caff", pg.BOOLEAN, server_default="false"))


def downgrade():
    op.drop_column("brew", "is_half_caff")
