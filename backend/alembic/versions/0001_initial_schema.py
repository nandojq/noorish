"""Initial schema

Revision ID: 0001
Revises:
Create Date: 2026-05-16

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ingredients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("aliases", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("season", sa.String(50), nullable=True),
        sa.Column("unit_weights", postgresql.JSONB(), nullable=True),
        sa.Column("density_g_per_ml", sa.Float(), nullable=True),
        sa.Column("nutrition_per_100g", postgresql.JSONB(), nullable=False),
        sa.Column("environmental_impact", postgresql.JSONB(), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.create_table(
        "recipes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.String(1000), nullable=True),
        sa.Column("servings", sa.Integer(), nullable=False),
        sa.Column("ingredients", postgresql.JSONB(), nullable=False),
        sa.Column("prep_instructions", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("cook_instructions", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("prep_time_minutes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("cook_time_minutes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tags", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("image_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="complete"),
        sa.Column("nutrition_total", postgresql.JSONB(), nullable=True),
        sa.Column("nutrition_per_serving", postgresql.JSONB(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("source", sa.String(50), nullable=False, server_default="manual"),
        sa.Column("source_url", sa.String(2048), nullable=True),
    )

    op.create_table(
        "images",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("data", sa.LargeBinary(), nullable=False),
        sa.Column("content_type", sa.String(50), nullable=False),
        sa.Column(
            "recipe_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("recipes.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    op.create_table(
        "menus",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("days", postgresql.JSONB(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.create_table(
        "user_settings",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("analysis", postgresql.JSONB(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("user_settings")
    op.drop_table("menus")
    op.drop_table("images")
    op.drop_table("recipes")
    op.drop_table("ingredients")
