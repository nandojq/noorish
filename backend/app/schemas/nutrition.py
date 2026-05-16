from __future__ import annotations

import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Macronutrients(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    protein: Optional[float] = None
    carbohydrates: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None
    sugar: Optional[float] = None
    saturated_fat: Optional[float] = None
    trans_fat: Optional[float] = None
    polyunsaturated_fat: Optional[float] = None
    monounsaturated_fat: Optional[float] = None
    added_sugars: Optional[float] = None
    cholesterol: Optional[float] = None


class Vitamins(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    vitamin_a: Optional[float] = None
    vitamin_c: Optional[float] = None
    vitamin_d: Optional[float] = None
    vitamin_e: Optional[float] = None
    vitamin_k: Optional[float] = None
    thiamine: Optional[float] = None
    riboflavin: Optional[float] = None
    niacin: Optional[float] = None
    vitamin_b6: Optional[float] = None
    folate: Optional[float] = None
    vitamin_b12: Optional[float] = None


class Minerals(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    calcium: Optional[float] = None
    iron: Optional[float] = None
    magnesium: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    zinc: Optional[float] = None
    copper: Optional[float] = None
    manganese: Optional[float] = None
    selenium: Optional[float] = None
    sodium: Optional[float] = None


class Micronutrients(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    vitamins: Optional[Vitamins] = None
    minerals: Optional[Minerals] = None


class NutritionPer100g(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    calories: Optional[float] = None
    macronutrients: Optional[Macronutrients] = None
    micronutrients: Optional[Micronutrients] = None


# NutritionBlock has the same structure as NutritionPer100g,
# reused for recipe totals and per-serving values.
class NutritionBlock(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    calories: Optional[float] = None
    macronutrients: Optional[Macronutrients] = None
    micronutrients: Optional[Micronutrients] = None


class DriComparisonEntry(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    nutrient: str
    daily_average_value: float
    dri_value: float
    unit: str
    percent_dv: float
    status: str  # "deficient" | "adequate" | "excess"


class DayNutrition(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    date: str  # YYYY-MM-DD
    nutrition_total: NutritionBlock


class MenuNutritionAnalysis(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    menu_id: uuid.UUID
    days: list[DayNutrition]
    period_total: NutritionBlock
    daily_average: NutritionBlock
    dri_comparison: list[DriComparisonEntry]
