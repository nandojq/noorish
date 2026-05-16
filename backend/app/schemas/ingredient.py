from __future__ import annotations

import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from app.schemas.nutrition import NutritionPer100g


class UnitWeights(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    small_unit_g: Optional[float] = None
    medium_unit_g: Optional[float] = None
    large_unit_g: Optional[float] = None


class IngredientMetadata(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    source: str  # "usda" | "edamam" | "open_food_facts" | "manual"
    source_id: Optional[str] = None
    last_updated: str  # ISO 8601 timestamp
    data_quality: Optional[str] = None  # "high" | "medium" | "low"


class EnvironmentalImpact(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    carbon_g_co2e_per_kg: Optional[float] = None
    water_l_per_kg: Optional[float] = None
    land_m2_per_kg: Optional[float] = None


class IngredientCreate(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: str
    aliases: Optional[list[str]] = None
    category: str
    season: Optional[str] = None
    unit_weights: Optional[UnitWeights] = None
    density_g_per_ml: Optional[float] = None
    nutrition_per_100g: NutritionPer100g
    environmental_impact: Optional[EnvironmentalImpact] = None
    metadata: IngredientMetadata


class IngredientUpdate(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: Optional[str] = None
    aliases: Optional[list[str]] = None
    category: Optional[str] = None
    season: Optional[str] = None
    unit_weights: Optional[UnitWeights] = None
    density_g_per_ml: Optional[float] = None
    nutrition_per_100g: Optional[NutritionPer100g] = None
    environmental_impact: Optional[EnvironmentalImpact] = None
    metadata: Optional[IngredientMetadata] = None


class IngredientResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    id: uuid.UUID
    name: str
    aliases: Optional[list[str]] = None
    category: str
    season: Optional[str] = None
    unit_weights: Optional[UnitWeights] = None
    density_g_per_ml: Optional[float] = None
    nutrition_per_100g: NutritionPer100g
    environmental_impact: Optional[EnvironmentalImpact] = None
    metadata: IngredientMetadata = Field(validation_alias="ingredient_metadata")
