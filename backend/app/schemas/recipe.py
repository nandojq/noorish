from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

from app.schemas.nutrition import NutritionBlock


class RecipeIngredient(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    ingredient_id: uuid.UUID
    ingredient_name: str
    amount: float
    unit: str  # grams | ml | tsp | tbsp | cup | large_unit | medium_unit | small_unit


class RecipeMetadata(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    source: Optional[str] = None
    source_url: Optional[str] = None


class RecipeCreate(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: str
    description: Optional[str] = None
    servings: int
    ingredients: list[RecipeIngredient]
    prep_instructions: Optional[list[str]] = None
    cook_instructions: list[str]
    prep_time_minutes: int = 0
    cook_time_minutes: int = 0
    tags: Optional[list[str]] = None
    source: Optional[str] = "manual"
    source_url: Optional[str] = None

    @field_validator("servings")
    @classmethod
    def servings_must_be_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("servings must be >= 1")
        return v

    @field_validator("ingredients")
    @classmethod
    def ingredients_not_empty(cls, v: list) -> list:
        if len(v) < 1:
            raise ValueError("at least one ingredient is required")
        return v

    @field_validator("cook_instructions")
    @classmethod
    def cook_instructions_not_empty(cls, v: list) -> list:
        if len(v) < 1:
            raise ValueError("at least one cook instruction is required")
        return v


class RecipeUpdate(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: Optional[str] = None
    description: Optional[str] = None
    servings: Optional[int] = None
    ingredients: Optional[list[RecipeIngredient]] = None
    prep_instructions: Optional[list[str]] = None
    cook_instructions: Optional[list[str]] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    tags: Optional[list[str]] = None
    source: Optional[str] = None
    source_url: Optional[str] = None


class RecipeNutritionPreview(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    nutrition_total: Optional[NutritionBlock] = None
    nutrition_per_serving: Optional[NutritionBlock] = None


class RecipeResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    id: uuid.UUID
    name: str
    description: Optional[str] = None
    servings: int
    ingredients: list[RecipeIngredient]
    prep_instructions: Optional[list[str]] = None
    cook_instructions: list[str]
    prep_time_minutes: int
    cook_time_minutes: int
    tags: Optional[list[str]] = None
    image_id: Optional[uuid.UUID] = None
    status: str
    nutrition_total: Optional[NutritionBlock] = None
    nutrition_per_serving: Optional[NutritionBlock] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
