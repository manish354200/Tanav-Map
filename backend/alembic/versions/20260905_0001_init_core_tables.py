"""init core tables

Revision ID: 20260905_0001
Revises:
Create Date: 2026-09-05
"""

from alembic import op
import sqlalchemy as sa


revision = "20260905_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="counselor"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "victims",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("case_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="registered"),
        sa.Column("current_distress_score", sa.Float(), nullable=False, server_default="50"),
        sa.Column("risk_level", sa.String(length=20), nullable=False, server_default="medium"),
        sa.Column("registration_date", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "interactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("victim_id", sa.Integer(), sa.ForeignKey("victims.id"), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False, server_default="text"),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("channel", sa.String(length=50), nullable=False, server_default="chatbot"),
        sa.Column("audio_file_path", sa.String(length=255), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("processed", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("victim_id", sa.Integer(), sa.ForeignKey("victims.id"), nullable=False),
        sa.Column("level", sa.String(length=20), nullable=False, server_default="low"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.create_table(
        "interventions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("victim_id", sa.Integer(), sa.ForeignKey("victims.id"), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False, server_default="counseling"),
        sa.Column("priority", sa.String(length=20), nullable=False, server_default="medium"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "distress_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("victim_id", sa.Integer(), sa.ForeignKey("victims.id"), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("risk_level", sa.String(length=20), nullable=False),
        sa.Column("sentiment_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("voice_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("behavior_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("threat_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("history_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("distress_history")
    op.drop_table("interventions")
    op.drop_table("alerts")
    op.drop_table("interactions")
    op.drop_table("victims")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
