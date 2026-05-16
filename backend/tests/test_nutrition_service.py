"""Unit tests for the pure nutrition calculation service."""
import pytest

from app.services.nutrition import (
    convert_to_grams,
    add_nutrition_blocks,
    scale_nutrition_block,
    compute_recipe_nutrition,
    _zero_nutrition_block,
)


# ── convert_to_grams ──────────────────────────────────────────────────────────

def test_convert_grams():
    assert convert_to_grams(100, "grams", {}) == 100.0


def test_convert_tsp():
    assert convert_to_grams(1, "tsp", {}) == pytest.approx(4.2)


def test_convert_tbsp():
    assert convert_to_grams(2, "tbsp", {}) == pytest.approx(25.2)


def test_convert_cup():
    assert convert_to_grams(0.5, "cup", {}) == pytest.approx(120.0)


def test_convert_ml_uses_density():
    assert convert_to_grams(100, "ml", {"density_g_per_ml": 0.92}) == pytest.approx(92.0)


def test_convert_ml_defaults_to_1():
    assert convert_to_grams(100, "ml", {}) == pytest.approx(100.0)


def test_convert_large_unit():
    result = convert_to_grams(2, "large_unit", {"unit_weights": {"large_unit_g": 56}})
    assert result == pytest.approx(112.0)


def test_convert_medium_unit():
    result = convert_to_grams(1, "medium_unit", {"unit_weights": {"medium_unit_g": 50}})
    assert result == pytest.approx(50.0)


def test_convert_small_unit():
    result = convert_to_grams(3, "small_unit", {"unit_weights": {"small_unit_g": 38}})
    assert result == pytest.approx(114.0)


def test_convert_large_unit_missing_raises():
    with pytest.raises(ValueError, match="large_unit_g"):
        convert_to_grams(1, "large_unit", {"unit_weights": {}})


def test_convert_unknown_unit_raises():
    with pytest.raises(ValueError, match="Unknown unit"):
        convert_to_grams(1, "ounces", {})


# ── add_nutrition_blocks ──────────────────────────────────────────────────────

def test_add_blocks_sums_calories():
    a = _zero_nutrition_block()
    b = _zero_nutrition_block()
    a["calories"] = 100.0
    b["calories"] = 50.0
    result = add_nutrition_blocks(a, b)
    assert result["calories"] == pytest.approx(150.0)


def test_add_blocks_sums_macros():
    a = _zero_nutrition_block()
    b = _zero_nutrition_block()
    a["macronutrients"]["protein"] = 10.0
    b["macronutrients"]["protein"] = 5.0
    result = add_nutrition_blocks(a, b)
    assert result["macronutrients"]["protein"] == pytest.approx(15.0)


def test_add_blocks_handles_none_gracefully():
    a = {"calories": None, "macronutrients": {}, "micronutrients": {}}
    b = _zero_nutrition_block()
    b["calories"] = 30.0
    result = add_nutrition_blocks(a, b)
    assert result["calories"] == pytest.approx(30.0)


# ── scale_nutrition_block ─────────────────────────────────────────────────────

def test_scale_block_by_factor():
    block = _zero_nutrition_block()
    block["calories"] = 200.0
    block["macronutrients"]["protein"] = 10.0
    scaled = scale_nutrition_block(block, 0.5)
    assert scaled["calories"] == pytest.approx(100.0)
    assert scaled["macronutrients"]["protein"] == pytest.approx(5.0)


def test_scale_block_by_zero():
    block = _zero_nutrition_block()
    block["calories"] = 200.0
    scaled = scale_nutrition_block(block, 0.0)
    assert scaled["calories"] == pytest.approx(0.0)


# ── compute_recipe_nutrition ──────────────────────────────────────────────────

_APPLE_NUTRITION = {
    "calories": 52.0,
    "macronutrients": {"protein": 0.3, "carbohydrates": 13.8, "fat": 0.2,
                       "fiber": 2.4, "sugar": 10.4, "saturated_fat": 0.0,
                       "trans_fat": 0.0, "polyunsaturated_fat": 0.0,
                       "monounsaturated_fat": 0.0, "added_sugars": 0.0,
                       "cholesterol": 0.0},
    "micronutrients": {"vitamins": {"vitamin_a": 3.0, "vitamin_c": 4.6,
                                    "vitamin_d": 0.0, "vitamin_e": 0.2,
                                    "vitamin_k": 2.2, "thiamine": 0.017,
                                    "riboflavin": 0.026, "niacin": 0.091,
                                    "vitamin_b6": 0.041, "folate": 3.0,
                                    "vitamin_b12": 0.0},
                       "minerals": {"calcium": 6.0, "iron": 0.12, "magnesium": 5.0,
                                    "phosphorus": 11.0, "potassium": 107.0, "zinc": 0.04,
                                    "copper": 0.027, "manganese": 0.035,
                                    "selenium": 0.0, "sodium": 1.0}},
}

_INGREDIENT_MAP = {
    "apple-id": {
        "name": "Apple",
        "nutrition_per_100g": _APPLE_NUTRITION,
        "unit_weights": None,
        "density_g_per_ml": None,
    }
}


def test_compute_nutrition_single_ingredient():
    ingredients = [
        {"ingredient_id": "apple-id", "amount": 150.0, "unit": "grams"}
    ]
    total, per_serving = compute_recipe_nutrition(ingredients, _INGREDIENT_MAP, servings=1)
    assert total["calories"] == pytest.approx(52.0 * 1.5)


def test_compute_nutrition_per_serving():
    ingredients = [
        {"ingredient_id": "apple-id", "amount": 200.0, "unit": "grams"}
    ]
    total, per_serving = compute_recipe_nutrition(ingredients, _INGREDIENT_MAP, servings=2)
    assert per_serving["calories"] == pytest.approx(total["calories"] / 2)


def test_compute_nutrition_missing_ingredient_skipped():
    ingredients = [
        {"ingredient_id": "apple-id", "amount": 100.0, "unit": "grams"},
        {"ingredient_id": "missing-id", "amount": 100.0, "unit": "grams"},
    ]
    total, _ = compute_recipe_nutrition(ingredients, _INGREDIENT_MAP, servings=1)
    # Only apple contributes
    assert total["calories"] == pytest.approx(52.0)


def test_compute_nutrition_tsp_conversion():
    oil_nutrition = {
        "calories": 884.0,
        "macronutrients": {"protein": 0.0, "carbohydrates": 0.0, "fat": 100.0,
                           "fiber": 0.0, "sugar": 0.0, "saturated_fat": 14.0,
                           "trans_fat": 0.0, "polyunsaturated_fat": 10.0,
                           "monounsaturated_fat": 73.0, "added_sugars": 0.0,
                           "cholesterol": 0.0},
        "micronutrients": {"vitamins": {k: 0.0 for k in ["vitamin_a", "vitamin_c", "vitamin_d",
                                                           "vitamin_e", "vitamin_k", "thiamine",
                                                           "riboflavin", "niacin", "vitamin_b6",
                                                           "folate", "vitamin_b12"]},
                           "minerals": {k: 0.0 for k in ["calcium", "iron", "magnesium",
                                                           "phosphorus", "potassium", "zinc",
                                                           "copper", "manganese", "selenium",
                                                           "sodium"]}},
    }
    ingredient_map = {
        "oil-id": {
            "name": "Olive Oil",
            "nutrition_per_100g": oil_nutrition,
            "unit_weights": None,
            "density_g_per_ml": 0.92,
        }
    }
    # 1 tsp = 4.2g → calories = 884 * (4.2/100) ≈ 37.1
    ingredients = [{"ingredient_id": "oil-id", "amount": 1, "unit": "tsp"}]
    total, _ = compute_recipe_nutrition(ingredients, ingredient_map, servings=1)
    assert total["calories"] == pytest.approx(884.0 * 4.2 / 100, rel=1e-3)
