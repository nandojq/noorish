"""
Nutrition calculation service.

All amounts are converted to grams, then nutrition is scaled from
the ingredient's nutrition_per_100g values.
"""
from __future__ import annotations

from app.constants.dri import DRI, DRI_UNITS

# Fixed unit conversions to grams
UNIT_CONVERSIONS: dict[str, float] = {
    "grams": 1.0,
    "tsp": 4.2,
    "tbsp": 12.6,
    "cup": 240.0,
}


def convert_to_grams(amount: float, unit: str, ingredient_data: dict) -> float:
    """
    Convert an ingredient amount in the given unit to grams.

    Supported units:
    - grams, tsp, tbsp, cup  — fixed constants
    - ml                     — uses ingredient density_g_per_ml (default 1.0)
    - large_unit, medium_unit, small_unit — use ingredient unit_weights fields

    Raises ValueError for unsupported units or missing unit_weight entries.
    """
    if unit in UNIT_CONVERSIONS:
        return amount * UNIT_CONVERSIONS[unit]

    if unit == "ml":
        density = ingredient_data.get("density_g_per_ml") or 1.0
        return amount * density

    unit_weights = ingredient_data.get("unit_weights") or {}

    if unit == "large_unit":
        value = unit_weights.get("large_unit_g")
        if value is None:
            raise ValueError(
                f"Ingredient '{ingredient_data.get('name', '')}' has no large_unit_g defined"
            )
        return amount * float(value)

    if unit == "medium_unit":
        value = unit_weights.get("medium_unit_g")
        if value is None:
            raise ValueError(
                f"Ingredient '{ingredient_data.get('name', '')}' has no medium_unit_g defined"
            )
        return amount * float(value)

    if unit == "small_unit":
        value = unit_weights.get("small_unit_g")
        if value is None:
            raise ValueError(
                f"Ingredient '{ingredient_data.get('name', '')}' has no small_unit_g defined"
            )
        return amount * float(value)

    raise ValueError(f"Unknown unit '{unit}'")


def _zero_nutrition_block() -> dict:
    """Return a NutritionBlock dict with all values initialised to 0.0."""
    return {
        "calories": 0.0,
        "macronutrients": {
            "protein": 0.0,
            "carbohydrates": 0.0,
            "fat": 0.0,
            "fiber": 0.0,
            "sugar": 0.0,
            "saturated_fat": 0.0,
            "trans_fat": 0.0,
            "polyunsaturated_fat": 0.0,
            "monounsaturated_fat": 0.0,
            "added_sugars": 0.0,
            "cholesterol": 0.0,
        },
        "micronutrients": {
            "vitamins": {
                "vitamin_a": 0.0,
                "vitamin_c": 0.0,
                "vitamin_d": 0.0,
                "vitamin_e": 0.0,
                "vitamin_k": 0.0,
                "thiamine": 0.0,
                "riboflavin": 0.0,
                "niacin": 0.0,
                "vitamin_b6": 0.0,
                "folate": 0.0,
                "vitamin_b12": 0.0,
            },
            "minerals": {
                "calcium": 0.0,
                "iron": 0.0,
                "magnesium": 0.0,
                "phosphorus": 0.0,
                "potassium": 0.0,
                "zinc": 0.0,
                "copper": 0.0,
                "manganese": 0.0,
                "selenium": 0.0,
                "sodium": 0.0,
            },
        },
    }


def add_nutrition_blocks(a: dict, b: dict) -> dict:
    """Element-wise addition of two NutritionBlock dicts."""
    result = _zero_nutrition_block()

    result["calories"] = (a.get("calories") or 0.0) + (b.get("calories") or 0.0)

    a_macro = a.get("macronutrients") or {}
    b_macro = b.get("macronutrients") or {}
    for key in result["macronutrients"]:
        result["macronutrients"][key] = (a_macro.get(key) or 0.0) + (
            b_macro.get(key) or 0.0
        )

    a_micro = a.get("micronutrients") or {}
    b_micro = b.get("micronutrients") or {}

    a_vitamins = a_micro.get("vitamins") or {}
    b_vitamins = b_micro.get("vitamins") or {}
    for key in result["micronutrients"]["vitamins"]:
        result["micronutrients"]["vitamins"][key] = (
            a_vitamins.get(key) or 0.0
        ) + (b_vitamins.get(key) or 0.0)

    a_minerals = a_micro.get("minerals") or {}
    b_minerals = b_micro.get("minerals") or {}
    for key in result["micronutrients"]["minerals"]:
        result["micronutrients"]["minerals"][key] = (
            a_minerals.get(key) or 0.0
        ) + (b_minerals.get(key) or 0.0)

    return result


def scale_nutrition_block(block: dict, factor: float) -> dict:
    """Multiply all values in a NutritionBlock by the given factor."""
    result = _zero_nutrition_block()

    result["calories"] = (block.get("calories") or 0.0) * factor

    macro = block.get("macronutrients") or {}
    for key in result["macronutrients"]:
        result["macronutrients"][key] = (macro.get(key) or 0.0) * factor

    micro = block.get("micronutrients") or {}
    vitamins = micro.get("vitamins") or {}
    for key in result["micronutrients"]["vitamins"]:
        result["micronutrients"]["vitamins"][key] = (vitamins.get(key) or 0.0) * factor

    minerals = micro.get("minerals") or {}
    for key in result["micronutrients"]["minerals"]:
        result["micronutrients"]["minerals"][key] = (
            minerals.get(key) or 0.0
        ) * factor

    return result


def _scale_per_100g_to_grams(
    nutrition_per_100g: dict, grams: float
) -> dict:
    """Scale nutrition_per_100g values to the actual gram amount."""
    factor = grams / 100.0
    return scale_nutrition_block(nutrition_per_100g, factor)


def compute_recipe_nutrition(
    ingredients: list[dict],
    ingredient_map: dict[str, dict],
    servings: int,
) -> tuple[dict, dict]:
    """
    Compute nutrition_total and nutrition_per_serving for a recipe.

    Args:
        ingredients: list of {ingredient_id, ingredient_name, amount, unit}
        ingredient_map: dict mapping ingredient_id (str) -> ingredient DB row as dict
        servings: number of servings

    Returns:
        (nutrition_total, nutrition_per_serving) as NutritionBlock dicts
    """
    total = _zero_nutrition_block()

    for row in ingredients:
        ingredient_id = str(row.get("ingredient_id") or row.get("ingredientId", ""))
        ingredient_data = ingredient_map.get(ingredient_id)
        if ingredient_data is None:
            # Skip missing ingredients (incomplete recipe handling)
            continue

        amount = float(row.get("amount", 0))
        unit = row.get("unit", "grams")

        grams = convert_to_grams(amount, unit, ingredient_data)
        nutrition_per_100g = ingredient_data.get("nutrition_per_100g") or {}
        contribution = _scale_per_100g_to_grams(nutrition_per_100g, grams)
        total = add_nutrition_blocks(total, contribution)

    per_serving = scale_nutrition_block(total, 1.0 / max(servings, 1))
    return total, per_serving


def _get_flat_nutrients(block: dict) -> dict[str, float]:
    """
    Flatten a NutritionBlock into a {nutrient_key: value} dict
    matching the DRI key names.
    """
    flat: dict[str, float] = {}

    flat["calories"] = block.get("calories") or 0.0

    macro = block.get("macronutrients") or {}
    for key in [
        "protein", "carbohydrates", "fat", "fiber",
        "saturated_fat", "cholesterol",
    ]:
        flat[key] = macro.get(key) or 0.0

    micro = block.get("micronutrients") or {}
    vitamins = micro.get("vitamins") or {}
    for key in [
        "vitamin_a", "vitamin_c", "vitamin_d", "vitamin_e", "vitamin_k",
        "thiamine", "riboflavin", "niacin", "vitamin_b6", "folate", "vitamin_b12",
    ]:
        flat[key] = vitamins.get(key) or 0.0

    minerals = micro.get("minerals") or {}
    for key in [
        "calcium", "iron", "magnesium", "phosphorus", "potassium",
        "zinc", "copper", "manganese", "selenium", "sodium",
    ]:
        flat[key] = minerals.get(key) or 0.0

    return flat


def compute_menu_nutrition_analysis(
    menu: dict,
    recipe_map: dict[str, dict],
    settings: dict,
) -> dict:
    """
    Compute the full MenuNutritionAnalysis for a menu.

    Args:
        menu: menu row as dict (with 'id', 'days' list)
        recipe_map: dict mapping recipe_id (str) -> recipe dict (with nutrition_total stored)
        settings: {deficiency_threshold_percent_dv, excess_threshold_percent_dv}

    Returns:
        MenuNutritionAnalysis dict (not stored)
    """
    deficiency_threshold = settings.get("deficiency_threshold_percent_dv", 70)
    excess_threshold = settings.get("excess_threshold_percent_dv", 150)

    days_output = []
    period_total = _zero_nutrition_block()

    days = menu.get("days") or []

    for day in days:
        day_total = _zero_nutrition_block()
        meals = day.get("meals") or {}
        for slot in ["breakfast", "lunch", "dinner", "snack"]:
            for recipe_id in meals.get(slot) or []:
                recipe = recipe_map.get(str(recipe_id))
                if recipe is None:
                    continue
                nutrition_total = recipe.get("nutrition_total") or {}
                day_total = add_nutrition_blocks(day_total, nutrition_total)

        days_output.append(
            {
                "date": day.get("date", ""),
                "nutrition_total": day_total,
            }
        )
        period_total = add_nutrition_blocks(period_total, day_total)

    num_days = max(len(days_output), 1)
    daily_average = scale_nutrition_block(period_total, 1.0 / num_days)

    # Build DRI comparison
    flat_daily = _get_flat_nutrients(daily_average)
    dri_comparison = []

    for nutrient, dri_value in DRI.items():
        daily_value = flat_daily.get(nutrient, 0.0)
        unit = DRI_UNITS.get(nutrient, "")
        if dri_value > 0:
            percent_dv = round((daily_value / dri_value) * 100, 2)
        else:
            percent_dv = 0.0

        if percent_dv < deficiency_threshold:
            status = "deficient"
        elif percent_dv > excess_threshold:
            status = "excess"
        else:
            status = "adequate"

        dri_comparison.append(
            {
                "nutrient": nutrient,
                "daily_average_value": round(daily_value, 4),
                "dri_value": dri_value,
                "unit": unit,
                "percent_dv": percent_dv,
                "status": status,
            }
        )

    return {
        "menu_id": str(menu.get("id", "")),
        "days": days_output,
        "period_total": period_total,
        "daily_average": daily_average,
        "dri_comparison": dri_comparison,
    }
