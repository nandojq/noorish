"""Integration tests for /api/menus endpoints."""
import pytest
from httpx import AsyncClient

from tests.conftest import INGREDIENT_PAYLOAD


async def _create_ingredient(client: AsyncClient, name: str = "Apple") -> dict:
    payload = {**INGREDIENT_PAYLOAD, "name": name}
    r = await client.post("/api/ingredients", json=payload)
    assert r.status_code == 201, r.text
    return r.json()


async def _create_recipe(client: AsyncClient, ingredient_id: str, name: str = "Apple Pie") -> dict:
    r = await client.post(
        "/api/recipes",
        json={
            "name": name,
            "servings": 2,
            "ingredients": [
                {
                    "ingredientId": ingredient_id,
                    "ingredientName": "Apple",
                    "amount": 150,
                    "unit": "grams",
                }
            ],
            "cookInstructions": ["Cook"],
            "prepTimeMinutes": 5,
            "cookTimeMinutes": 20,
        },
    )
    assert r.status_code == 201, r.text
    return r.json()


async def _create_menu(client: AsyncClient, name: str = "Week 1") -> dict:
    r = await client.post(
        "/api/menus",
        json={"name": name, "startDate": "2026-05-19", "endDate": "2026-05-25"},
    )
    assert r.status_code == 201, r.text
    return r.json()


# ── CRUD ──────────────────────────────────────────────────────────────────────

async def test_list_menus_empty(client: AsyncClient):
    r = await client.get("/api/menus")
    assert r.status_code == 200
    assert r.json() == []


async def test_create_menu(client: AsyncClient):
    r = await client.post(
        "/api/menus",
        json={"name": "My Menu", "startDate": "2026-05-19", "endDate": "2026-05-25"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "My Menu"
    assert data["startDate"] == "2026-05-19"
    assert data["days"] == []


async def test_create_menu_invalid_dates(client: AsyncClient):
    r = await client.post(
        "/api/menus",
        json={"name": "Bad", "startDate": "2026-05-25", "endDate": "2026-05-19"},
    )
    assert r.status_code == 422


async def test_get_menu(client: AsyncClient):
    menu = await _create_menu(client)
    r = await client.get(f"/api/menus/{menu['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == menu["id"]


async def test_get_menu_not_found(client: AsyncClient):
    r = await client.get("/api/menus/00000000-0000-0000-0000-000000000001")
    assert r.status_code == 404


async def test_update_menu_name(client: AsyncClient):
    menu = await _create_menu(client)
    r = await client.put(f"/api/menus/{menu['id']}", json={"name": "Updated"})
    assert r.status_code == 200
    assert r.json()["name"] == "Updated"


async def test_update_menu_assign_recipe(client: AsyncClient):
    ing = await _create_ingredient(client)
    recipe = await _create_recipe(client, ing["id"])
    menu = await _create_menu(client)

    r = await client.put(
        f"/api/menus/{menu['id']}",
        json={
            "days": [
                {
                    "date": "2026-05-19",
                    "meals": {
                        "breakfast": [recipe["id"]],
                        "lunch": [],
                        "dinner": [],
                        "snack": [],
                    },
                }
            ]
        },
    )
    assert r.status_code == 200
    breakfast = r.json()["days"][0]["meals"]["breakfast"]
    assert recipe["id"] in breakfast


async def test_update_menu_incomplete_recipe_rejected(client: AsyncClient):
    ing = await _create_ingredient(client)
    recipe = await _create_recipe(client, ing["id"])
    # Delete ingredient to make recipe incomplete
    await client.delete(f"/api/ingredients/{ing['id']}")

    menu = await _create_menu(client)
    r = await client.put(
        f"/api/menus/{menu['id']}",
        json={
            "days": [
                {
                    "date": "2026-05-19",
                    "meals": {
                        "breakfast": [recipe["id"]],
                        "lunch": [],
                        "dinner": [],
                        "snack": [],
                    },
                }
            ]
        },
    )
    assert r.status_code == 400


async def test_delete_menu(client: AsyncClient):
    menu = await _create_menu(client)
    r = await client.delete(f"/api/menus/{menu['id']}")
    assert r.status_code == 204
    assert (await client.get(f"/api/menus/{menu['id']}")).status_code == 404


# ── nutrition analysis ────────────────────────────────────────────────────────

async def test_menu_nutrition_empty_menu_returns_422(client: AsyncClient):
    menu = await _create_menu(client)
    r = await client.get(f"/api/menus/{menu['id']}/nutrition")
    assert r.status_code == 422


async def test_menu_nutrition_returns_analysis(client: AsyncClient):
    ing = await _create_ingredient(client)
    recipe = await _create_recipe(client, ing["id"])
    menu = await _create_menu(client)

    await client.put(
        f"/api/menus/{menu['id']}",
        json={
            "days": [
                {
                    "date": "2026-05-19",
                    "meals": {
                        "breakfast": [recipe["id"]],
                        "lunch": [],
                        "dinner": [],
                        "snack": [],
                    },
                }
            ]
        },
    )

    r = await client.get(f"/api/menus/{menu['id']}/nutrition")
    assert r.status_code == 200
    data = r.json()
    assert "driComparison" in data
    assert "dailyAverage" in data
    assert "periodTotal" in data
    assert len(data["days"]) == 1
    # Verify calories are non-zero (150g apple / 2 servings per recipe)
    assert data["periodTotal"]["calories"] > 0


async def test_menu_nutrition_dri_comparison_has_all_nutrients(client: AsyncClient):
    ing = await _create_ingredient(client)
    recipe = await _create_recipe(client, ing["id"])
    menu = await _create_menu(client)
    await client.put(
        f"/api/menus/{menu['id']}",
        json={
            "days": [
                {
                    "date": "2026-05-19",
                    "meals": {"breakfast": [recipe["id"]], "lunch": [], "dinner": [], "snack": []},
                }
            ]
        },
    )
    r = await client.get(f"/api/menus/{menu['id']}/nutrition")
    nutrients = {entry["nutrient"] for entry in r.json()["driComparison"]}
    assert "calories" in nutrients
    assert "protein" in nutrients
    assert "vitamin_c" in nutrients
    assert "calcium" in nutrients


# ── grocery list ──────────────────────────────────────────────────────────────

async def test_grocery_list_empty_menu_returns_422(client: AsyncClient):
    menu = await _create_menu(client)
    r = await client.get(f"/api/menus/{menu['id']}/grocery-list")
    assert r.status_code == 422


async def test_grocery_list_aggregates_ingredients(client: AsyncClient):
    ing = await _create_ingredient(client)
    recipe = await _create_recipe(client, ing["id"])
    menu = await _create_menu(client)

    # Assign same recipe twice (Mon breakfast + Mon lunch)
    await client.put(
        f"/api/menus/{menu['id']}",
        json={
            "days": [
                {
                    "date": "2026-05-19",
                    "meals": {
                        "breakfast": [recipe["id"]],
                        "lunch": [recipe["id"]],
                        "dinner": [],
                        "snack": [],
                    },
                }
            ]
        },
    )

    r = await client.get(f"/api/menus/{menu['id']}/grocery-list")
    assert r.status_code == 200
    data = r.json()
    assert data["menuId"] == menu["id"]
    assert len(data["items"]) == 1
    item = data["items"][0]
    assert item["ingredientName"] == "Apple"
    # 150g × 2 occurrences = 300g
    assert item["totalGrams"] == pytest.approx(300.0, rel=0.01)
