import uuid
from datetime import datetime

from sqlalchemy import String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    aliases: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    season: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # JSONB: {small_unit_g, medium_unit_g, large_unit_g}
    unit_weights: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    density_g_per_ml: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Full nutrition structure per 100g
    nutrition_per_100g: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Optional environmental impact
    environmental_impact: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Metadata: {source, source_id, last_updated, data_quality}
    # "metadata" is reserved by SQLAlchemy's DeclarativeBase; use ingredient_metadata as the attribute name
    ingredient_metadata: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False)

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
