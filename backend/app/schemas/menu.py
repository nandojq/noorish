from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel


class MealSlots(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    breakfast: list[str] = []
    lunch: list[str] = []
    dinner: list[str] = []
    snack: list[str] = []


class MenuDay(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    date: str  # YYYY-MM-DD
    meals: MealSlots = MealSlots()


class MenuCreate(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: str
    start_date: date
    end_date: date

    @field_validator("end_date")
    @classmethod
    def end_date_not_before_start(cls, v: date, info) -> date:
        start = info.data.get("start_date")
        if start is not None and v < start:
            raise ValueError("endDate must be >= startDate")
        return v


class MenuUpdate(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    days: Optional[list[MenuDay]] = None


class MenuResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    id: uuid.UUID
    name: str
    start_date: date
    end_date: date
    days: list[MenuDay] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GroceryItem(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    ingredient_id: uuid.UUID
    ingredient_name: str
    category: str
    total_grams: float


class GroceryListResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    menu_id: uuid.UUID
    items: list[GroceryItem]
