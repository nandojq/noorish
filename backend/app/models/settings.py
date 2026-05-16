from sqlalchemy import Integer, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    # Single-row table — use a fixed integer PK of 1
    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)

    # {deficiency_threshold_percent_dv: int, excess_threshold_percent_dv: int}
    analysis: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "deficiency_threshold_percent_dv": 70,
            "excess_threshold_percent_dv": 150,
        },
    )

    updated_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
