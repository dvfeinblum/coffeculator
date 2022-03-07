"""espresso deets

Revision ID: b2b34cb52a8d
Revises: d3f2978ed35f
Create Date: 2022-03-06 20:51:05.898791

"""
from alembic import op
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects import postgresql as pg


# revision identifiers, used by Alembic.

revision = "b2b34cb52a8d"
down_revision = "d3f2978ed35f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "espresso_detail",
        Column(
            "brew", pg.INTEGER, ForeignKey("brew.id"), primary_key=True, nullable=False
        ),
        Column("ratio", pg.TEXT),
        Column("preinfusion_duration", pg.INTERVAL),
    )


def downgrade():
    op.drop_table("espresso_detail")
