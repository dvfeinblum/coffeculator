"""grind stuff

Revision ID: f22183da93ae
Revises: 75608384762b
Create Date: 2022-02-28 10:17:53.739799

"""
import enum

from alembic import op
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql as pg


# revision identifiers, used by Alembic.

revision = "f22183da93ae"
down_revision = "75608384762b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("brew", Column("grinder", pg.TEXT))
    op.add_column("brew", Column("grind_setting", pg.TEXT))
    op.add_column("brew", Column("thoughts", pg.TEXT))


def downgrade():
    op.drop_column("brew", "grinder")
    op.drop_column("brew", "grind_setting")
    grinder = pg.ENUM("1zspresso jx-pro", "baratza encore", name="grinder")
    grinder.drop(op.get_bind())
