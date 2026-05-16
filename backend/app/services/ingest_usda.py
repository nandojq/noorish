"""
USDA FoodData Central ingest service.

Handles searching and importing ingredients from the USDA FDC API.
"""
from __future__ import annotations

from datetime import datetime, timezone

import httpx

USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1"

# Maps USDA nutrient name -> dot-path in NutritionPer100g structure
USDA_NUTRIENT_MAP: dict[str, str] = {
    "Energy": "calories",
    "Protein": "macronutrients.protein",
    "Total lipid (fat)": "macronutrients.fat",
    "Carbohydrate, by difference": "macronutrients.carbohydrates",
    "Fiber, total dietary": "macronutrients.fiber",
    "Sugars, total including NLEA": "macronutrients.sugar",
    "Fatty acids, total saturated": "macronutrients.saturated_fat",
    "Fatty acids, total trans": "macronutrients.trans_fat",
    "Fatty acids, total polyunsaturated": "macronutrients.polyunsaturated_fat",
    "Fatty acids, total monounsaturated": "macronutrients.monounsaturated_fat",
    "Cholesterol": "macronutrients.cholesterol",
    "Sodium, Na": "micronutrients.minerals.sodium",
    "Calcium, Ca": "micronutrients.minerals.calcium",
    "Iron, Fe": "micronutrients.minerals.iron",
    "Magnesium, Mg": "micronutrients.minerals.magnesium",
    "Phosphorus, P": "micronutrients.minerals.phosphorus",
    "Potassium, K": "micronutrients.minerals.potassium",
    "Zinc, Zn": "micronutrients.minerals.zinc",
    "Copper, Cu": "micronutrients.minerals.copper",
    "Manganese, Mn": "micronutrients.minerals.manganese",
    "Selenium, Se": "micronutrients.minerals.selenium",
    "Vitamin A, RAE": "micronutrients.vitamins.vitamin_a",
    "Vitamin C, total ascorbic acid": "micronutrients.vitamins.vitamin_c",
    "Vitamin D (D2 + D3)": "micronutrients.vitamins.vitamin_d",
    "Vitamin E (alpha-tocopherol)": "micronutrients.vitamins.vitamin_e",
    "Vitamin K (phylloquinone)": "micronutrients.vitamins.vitamin_k",
    "Thiamin": "micronutrients.vitamins.thiamine",
    "Riboflavin": "micronutrients.vitamins.riboflavin",
    "Niacin": "micronutrients.vitamins.niacin",
    "Vitamin B-6": "micronutrients.vitamins.vitamin_b6",
    "Folate, DFE": "micronutrients.vitamins.folate",
    "Vitamin B-12": "micronutrients.vitamins.vitamin_b12",
}

# Data quality per USDA data type
DATA_TYPE_QUALITY: dict[str, str] = {
    "Foundation": "high",
    "SR Legacy": "medium",
}

# Category mapping from USDA food categories to Noorish categories
USDA_CATEGORY_MAP: dict[str, str] = {
    "Poultry Products": "protein",
    "Beef Products": "protein",
    "Pork Products": "protein",
    "Finfish and Shellfish Products": "protein",
    "Lamb, Veal, and Game Products": "protein",
    "Sausages and Luncheon Meats": "protein",
    "Legumes and Legume Products": "protein",
    "Nut and Seed Products": "protein",
    "Vegetables and Vegetable Products": "vegetable",
    "Fruits and Fruit Juices": "fruit",
    "Dairy and Egg Products": "dairy",
    "Fats and Oils": "fat_and_oil",
    "Soups, Sauces, and Gravies": "condiment_and_sauce",
    "Spices and Herbs": "herb_and_spice",
    "Beverages": "beverage",
    "Snacks": "snack",
    "Cereal Grains and Pasta": "grain_and_cereal",
    "Breakfast Cereals": "grain_and_cereal",
    "Baked Products": "grain_and_cereal",
    "Sweets": "snack",
    "Meals, Entrees, and Side Dishes": "snack",
    "Fast Foods": "snack",
    "Restaurant Foods": "snack",
}


def _map_category(usda_category: str | None) -> str:
    """Map a USDA category string to a Noorish category enum value."""
    if not usda_category:
        return "snack"
    for usda_key, noorish_cat in USDA_CATEGORY_MAP.items():
        if usda_key.lower() in usda_category.lower():
            return noorish_cat
    return "snack"


def _build_nutrition_per_100g(nutrients: list[dict]) -> dict:
    """
    Build the nutrition_per_100g dict from a USDA nutrients array.
    Each nutrient has: {nutrientName, value, unitName}.
    """
    nutrition: dict = {
        "calories": None,
        "macronutrients": {
            "protein": None,
            "carbohydrates": None,
            "fat": None,
            "fiber": None,
            "sugar": None,
            "saturated_fat": None,
            "trans_fat": None,
            "polyunsaturated_fat": None,
            "monounsaturated_fat": None,
            "added_sugars": None,
            "cholesterol": None,
        },
        "micronutrients": {
            "vitamins": {
                "vitamin_a": None,
                "vitamin_c": None,
                "vitamin_d": None,
                "vitamin_e": None,
                "vitamin_k": None,
                "thiamine": None,
                "riboflavin": None,
                "niacin": None,
                "vitamin_b6": None,
                "folate": None,
                "vitamin_b12": None,
            },
            "minerals": {
                "calcium": None,
                "iron": None,
                "magnesium": None,
                "phosphorus": None,
                "potassium": None,
                "zinc": None,
                "copper": None,
                "manganese": None,
                "selenium": None,
                "sodium": None,
            },
        },
    }

    for nutrient in nutrients:
        name = nutrient.get("nutrientName") or nutrient.get("name", "")
        value = nutrient.get("value")
        if value is None:
            continue
        value = float(value)

        path = USDA_NUTRIENT_MAP.get(name)
        if path is None:
            continue

        parts = path.split(".")
        if len(parts) == 1:
            nutrition[parts[0]] = value
        elif len(parts) == 2:
            if parts[0] in nutrition and isinstance(nutrition[parts[0]], dict):
                nutrition[parts[0]][parts[1]] = value
        elif len(parts) == 3:
            sub = nutrition.get(parts[0], {})
            if isinstance(sub, dict):
                sub2 = sub.get(parts[1], {})
                if isinstance(sub2, dict):
                    sub2[parts[2]] = value

    return nutrition


async def search_usda(query: str, api_key: str) -> list[dict]:
    """
    Search USDA FoodData Central by name.
    Returns a list of candidate dicts (not persisted).
    """
    params = {
        "query": query,
        "dataType": "Foundation,SR Legacy",
        "pageSize": 10,
        "api_key": api_key,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                f"{USDA_BASE_URL}/foods/search",
                params=params,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"USDA API error: {exc.response.status_code}"
            ) from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"USDA API unreachable: {exc}") from exc

    data = response.json()
    foods = data.get("foods") or []

    results = []
    for food in foods:
        data_type = food.get("dataType", "")
        data_quality = DATA_TYPE_QUALITY.get(data_type, "medium")
        results.append(
            {
                "fdcId": str(food.get("fdcId", "")),
                "name": food.get("description", ""),
                "category": food.get("foodCategory", ""),
                "dataType": data_type,
                "dataQuality": data_quality,
            }
        )

    return results


async def import_usda(
    fdc_id: str,
    api_key: str,
    name_override: str | None = None,
) -> dict:
    """
    Fetch a single USDA food by fdcId, map to the Ingredient schema, and return
    the mapped dict ready for DB insert (id and timestamps must be added by caller).
    """
    params = {"api_key": api_key}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                f"{USDA_BASE_URL}/food/{fdc_id}",
                params=params,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"USDA API error: {exc.response.status_code}"
            ) from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"USDA API unreachable: {exc}") from exc

    food = response.json()

    data_type = food.get("dataType", "")
    data_quality = DATA_TYPE_QUALITY.get(data_type, "medium")

    name = name_override or food.get("description", "")
    category_raw = food.get("foodCategory")
    if isinstance(category_raw, dict):
        category_raw = category_raw.get("description", "")
    category = _map_category(category_raw)

    nutrients = food.get("foodNutrients") or []
    nutrition_per_100g = _build_nutrition_per_100g(nutrients)

    return {
        "name": name,
        "aliases": [],
        "category": category,
        "season": None,
        "unit_weights": None,
        "density_g_per_ml": None,
        "nutrition_per_100g": nutrition_per_100g,
        "environmental_impact": None,
        "metadata": {
            "source": "usda",
            "source_id": str(fdc_id),
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "data_quality": data_quality,
        },
    }
