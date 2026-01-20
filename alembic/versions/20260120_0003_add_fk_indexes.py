"""add foreign key indexes

Revision ID: 20260120_0003
Revises: 20260120_0002
Create Date: 2026-01-20 00:03:00

"""
from __future__ import annotations

from alembic import op

revision = "20260120_0003"
down_revision = "20260120_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add indexes on foreign key columns for better JOIN performance
    op.create_index("ix_students_school_id", "students", ["school_id"])
    op.create_index("ix_invoices_school_id", "invoices", ["school_id"])
    op.create_index("ix_invoices_student_id", "invoices", ["student_id"])
    op.create_index("ix_payments_invoice_id", "payments", ["invoice_id"])
    # Composite index for common invoice queries
    op.create_index("ix_invoices_student_status", "invoices", ["student_id", "status"])


def downgrade() -> None:
    op.drop_index("ix_invoices_student_status", table_name="invoices")
    op.drop_index("ix_payments_invoice_id", table_name="payments")
    op.drop_index("ix_invoices_student_id", table_name="invoices")
    op.drop_index("ix_invoices_school_id", table_name="invoices")
    op.drop_index("ix_students_school_id", table_name="students")
