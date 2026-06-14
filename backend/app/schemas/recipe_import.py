from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel


class RecipeImportIngredient(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    ingredient_id: Optional[str] = None
    ingredient_name: Optional[str] = None
    amount: float
    unit: str

    @field_validator("ingredient_name", mode="before")
    @classmethod
    def ingredient_name_required_if_no_id(cls, v, info):
        if not v and not info.data.get("ingredient_id"):
            raise ValueError("ingredientName is required when ingredientId is not provided")
        return v


class RecipeImportRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: str
    description: Optional[str] = None
    servings: int
    ingredients: list[RecipeImportIngredient]
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
