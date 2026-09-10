"""create shots

Revision ID: 0001
Revises:
Create Date: 2026-09-10
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "shots",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.String(1000), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="todo"),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_shots_title", "shots", ["title"])


def downgrade() -> None:
    op.drop_index("ix_shots_title", table_name="shots")
    op.drop_table("shots")
