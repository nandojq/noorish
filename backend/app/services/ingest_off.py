"""
Open Food Facts ingest service.

Handles searching and importing ingredients from the OFF API.
"""
from __future__ import annotations

from datetime import datetime, timezone

import httpx

OFF_BASE_URL = "https://world.openfoodfacts.org/api/v2"

# Maps OFF nutriments keys to NutritionPer100g dot-paths
# sodium in OFF is g/100g, must be converted to mg (×1000)
OFF_NUTRIENT_MAP: dict[str, tuple[str, float]] = {
    "energy-kcal_100g": ("calories", 1.0),
    "proteins_100g": ("macronutrients.protein", 1.0),
    "fat_100g": ("macronutrients.fat", 1.0),
    "carbohydrates_100g": ("macronutrients.carbohydrates", 1.0),
    "fiber_100g": ("macronutrients.fiber", 1.0),
    "sugars_100g": ("macronutrients.sugar", 1.0),
    "saturated-fat_100g": ("macronutrients.saturated_fat", 1.0),
    "trans-fat_100g": ("macronutrients.trans_fat", 1.0),
    "cholesterol_100g": ("macronutrients.cholesterol", 1000.0),  # g -> mg
    "sodium_100g": ("micronutrients.minerals.sodium", 1000.0),  # g -> mg
    "calcium_100g": ("micronutrients.minerals.calcium", 1000.0),  # g -> mg
    "iron_100g": ("micronutrients.minerals.iron", 1000.0),  # g -> mg
    "magnesium_100g": ("micronutrients.minerals.magnesium", 1000.0),  # g -> mg
    "phosphorus_100g": ("micronutrients.minerals.phosphorus", 1000.0),  # g -> mg
    "potassium_100g": ("micronutrients.minerals.potassium", 1000.0),  # g -> mg
    "zinc_100g": ("micronutrients.minerals.zinc", 1000.0),  # g -> mg
    "vitamin-c_100g": ("micronutrients.vitamins.vitamin_c", 1000.0),  # g -> mg
    "vitamin-a_100g": ("micronutrients.vitamins.vitamin_a", 1000000.0),  # g -> mcg
    "vitamin-d_100g": ("micronutrients.vitamins.vitamin_d", 1000000.0),  # g -> mcg
    "vitamin-e_100g": ("micronutrients.vitamins.vitamin_e", 1000.0),  # g -> mg
    "vitamin-k_100g": ("micronutrients.vitamins.vitamin_k", 1000000.0),  # g -> mcg
}

# Category mapping from OFF category tags to Noorish categories
OFF_CATEGORY_MAP: dict[str, str] = {
    "meats": "protein",
    "fish": "protein",
    "seafood": "protein",
    "legumes": "protein",
    "nuts": "protein",
    "eggs": "protein",
    "vegetables": "vegetable",
    "fruits": "fruit",
    "dairy": "dairy",
    "cheeses": "dairy",
    "milk": "dairy",
    "yogurts": "dairy",
    "oils": "fat_and_oil",
    "fats": "fat_and_oil",
    "sauces": "condiment_and_sauce",
    "condiments": "condiment_and_sauce",
    "spices": "herb_and_spice",
    "herbs": "herb_and_spice",
    "beverages": "beverage",
    "drinks": "beverage",
    "snacks": "snack",
    "cereals": "grain_and_cereal",
    "breads": "grain_and_cereal",
    "pasta": "grain_and_cereal",
    "rice": "grain_and_cereal",
    "grains": "grain_and_cereal",
}


def _map_off_category(categories_tags: list[str] | None) -> str:
    """Map OFF categories_tags to a Noorish category enum value."""
    if not categories_tags:
        return "snack"
    for tag in categories_tags:
        tag_lower = tag.lower()
        for key, cat in OFF_CATEGORY_MAP.items():
            if key in tag_lower:
                return cat
    return "snack"


def _build_nutrition_from_nutriments(nutriments: dict) -> dict:
    """
    Build the nutrition_per_100g structure from OFF nutriments dict.
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

    for off_key, (path, multiplier) in OFF_NUTRIENT_MAP.items():
        raw_value = nutriments.get(off_key)
        if raw_value is None:
            continue
        try:
            value = float(raw_value) * multiplier
        except (TypeError, ValueError):
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


def _map_product_to_ingredient(product: dict, name_override: str | None = None) -> dict:
    """Map a single OFF product dict to the Noorish ingredient structure."""
    name = name_override or product.get("product_name") or ""
    categories_tags = product.get("categories_tags") or []
    category = _map_off_category(categories_tags)
    source_id = product.get("_id") or product.get("id") or ""
    nutriments = product.get("nutriments") or {}
    nutrition_per_100g = _build_nutrition_from_nutriments(nutriments)

    return {
        "name": name,
        "aliases": [],
        "category": category,
        "season": None,
        "unit_weights": None,
        "density_g_per_ml": None,
        "nutrition_per_100g": nutrition_per_100g,
        "environmental_impact": None,
        "ingredient_metadata": {
            "source": "open_food_facts",
            "source_id": str(source_id),
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "data_quality": "medium",
        },
    }


async def search_off(query: str) -> list[dict]:
    """
    Search Open Food Facts by name.
    Returns candidate list (not persisted).
    """
    params = {
        "search_terms": query,
        "fields": "product_name,nutriments,categories_tags,_id",
        "page_size": 10,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                f"{OFF_BASE_URL}/search",
                params=params,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"OFF API error: {exc.response.status_code}"
            ) from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"OFF API unreachable: {exc}") from exc

    data = response.json()
    products = data.get("products") or []

    results = []
    for product in products:
        name = product.get("product_name") or ""
        if not name:
            continue
        off_id = product.get("_id") or product.get("id") or ""
        categories_tags = product.get("categories_tags") or []
        category = _map_off_category(categories_tags)
        results.append(
            {
                "offId": str(off_id),
                "name": name,
                "category": category,
                "dataQuality": "medium",
            }
        )

    return results


async def search_off_barcode(barcode: str) -> list[dict]:
    """
    Search Open Food Facts by barcode.
    Returns a single-item candidate list (not persisted).
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                f"{OFF_BASE_URL}/product/{barcode}.json",
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"OFF API error: {exc.response.status_code}"
            ) from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"OFF API unreachable: {exc}") from exc

    data = response.json()
    product = data.get("product")
    if not product:
        return []

    name = product.get("product_name") or ""
    off_id = product.get("_id") or product.get("id") or barcode
    categories_tags = product.get("categories_tags") or []
    category = _map_off_category(categories_tags)

    return [
        {
            "offId": str(off_id),
            "name": name,
            "category": category,
            "dataQuality": "medium",
        }
    ]


async def import_off(off_id: str, name_override: str | None = None) -> dict:
    """
    Fetch a single OFF product by ID (barcode), map to Ingredient schema.
    Returns the mapped dict ready for DB insert.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                f"{OFF_BASE_URL}/product/{off_id}.json",
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"OFF API error: {exc.response.status_code}"
            ) from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"OFF API unreachable: {exc}") from exc

    data = response.json()
    product = data.get("product")
    if not product:
        raise RuntimeError(f"OFF product '{off_id}' not found")

    return _map_product_to_ingredient(product, name_override)
