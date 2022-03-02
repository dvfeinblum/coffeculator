"""temp

Revision ID: d3f2978ed35f
Revises: f22183da93ae
Create Date: 2022-03-01 07:56:00.125725

"""
from alembic import op
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql as pg

# revision identifiers, used by Alembic.

revision = "d3f2978ed35f"
down_revision = "f22183da93ae"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("brew", Column("temperature", pg.INTEGER))


def downgrade():
    op.drop_column("brew", "temperature")
