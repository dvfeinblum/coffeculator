"""inital model

Revision ID: 75608384762b
Revises:
Create Date: 2022-02-27 19:58:48.873121

"""
from alembic import op
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects import postgresql as pg


# revision identifiers, used by Alembic.
revision = "75608384762b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "roaster",
        Column("id", pg.INTEGER, primary_key=True, autoincrement=True, nullable=False),
        Column("name", pg.TEXT),
        Column("location", pg.TEXT),
    )

    op.create_table(
        "coffee",
        Column("id", pg.INTEGER, primary_key=True, autoincrement=True, nullable=False),
        Column("name", pg.TEXT),
        Column("roaster", pg.INTEGER, ForeignKey("roaster.id")),
        Column("roast", pg.TEXT),
    )

    op.create_table(
        "brew",
        Column("id", pg.INTEGER, primary_key=True, autoincrement=True, nullable=False),
        Column("coffee", pg.INTEGER, ForeignKey("coffee.id")),
        Column("method", pg.TEXT),
        Column("dose", pg.NUMERIC),
        Column("coffee_out", pg.NUMERIC),
        Column("duration", pg.INTERVAL),
        Column("date", pg.TIMESTAMP, server_default=func.current_timestamp()),
    )


def downgrade():
    op.drop_table("brew")
    op.drop_table("coffee")
    op.drop_table("roaster")
