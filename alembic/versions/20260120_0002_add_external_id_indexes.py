"""add external_id indexes

Revision ID: 20260120_0002
Revises: 20260120_0001
Create Date: 2026-01-20 00:02:00

"""
from __future__ import annotations

from alembic import op

revision = "20260120_0002"
down_revision = "20260120_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_schools_external_id", "schools", ["external_id"])
    op.create_index("ix_students_external_id", "students", ["external_id"])


def downgrade() -> None:
    op.drop_index("ix_students_external_id", table_name="students")
    op.drop_index("ix_schools_external_id", table_name="schools")
