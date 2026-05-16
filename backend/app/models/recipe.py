import uuid
from datetime import datetime

from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, LargeBinary, func
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Image(Base):
    __tablename__ = "images"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False)
    recipe_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipes.id", ondelete="SET NULL"),
        nullable=True,
    )

    recipe: Mapped["Recipe | None"] = relationship(
        "Recipe",
        back_populates="image",
        foreign_keys=[recipe_id],
    )


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    servings: Mapped[int] = mapped_column(Integer, nullable=False)

    # JSONB array: [{ingredient_id, ingredient_name, amount, unit}]
    ingredients: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # Optional ordered steps
    prep_instructions: Mapped[list[str] | None] = mapped_column(
        ARRAY(String), nullable=True
    )
    # Required, >= 1
    cook_instructions: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False
    )

    prep_time_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cook_time_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    image_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    # "complete" | "incomplete" — set by backend, never by client
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="complete"
    )

    # Computed and stored on every create/update
    nutrition_total: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    nutrition_per_serving: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="manual")
    source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    image: Mapped["Image | None"] = relationship(
        "Image",
        back_populates="recipe",
        foreign_keys="[Image.recipe_id]",
        uselist=False,
    )
