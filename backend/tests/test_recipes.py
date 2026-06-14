"""Integration tests for /api/recipes endpoints."""
import pytest
from httpx import AsyncClient

from tests.conftest import INGREDIENT_PAYLOAD, MINIMAL_NUTRITION


async def _create_ingredient(client: AsyncClient, name: str = "Apple") -> dict:
    payload = {**INGREDIENT_PAYLOAD, "name": name}
    r = await client.post("/api/ingredients", json=payload)
    assert r.status_code == 201, r.text
    return r.json()


def _recipe_payload(ingredient_id: str, name: str = "Apple Pie", servings: int = 4) -> dict:
    return {
        "name": name,
        "servings": servings,
        "ingredients": [
            {
                "ingredientId": ingredient_id,
                "ingredientName": "Apple",
                "amount": 200,
                "unit": "grams",
            }
        ],
        "cookInstructions": ["Bake at 180°C for 30 minutes"],
        "prepTimeMinutes": 15,
        "cookTimeMinutes": 30,
    }


# ── list ──────────────────────────────────────────────────────────────────────

async def test_list_recipes_empty(client: AsyncClient):
    r = await client.get("/api/recipes")
    assert r.status_code == 200
    assert r.json() == []


async def test_list_recipes_filter_by_status(client: AsyncClient):
    ing = await _create_ingredient(client)
    await client.post("/api/recipes", json=_recipe_payload(ing["id"]))
    r = await client.get("/api/recipes?status=complete")
    assert r.status_code == 200
    assert len(r.json()) == 1
    r2 = await client.get("/api/recipes?status=incomplete")
    assert r2.json() == []


async def test_list_recipes_search_by_name(client: AsyncClient):
    ing = await _create_ingredient(client)
    await client.post("/api/recipes", json=_recipe_payload(ing["id"], "Apple Pie"))
    await client.post("/api/recipes", json=_recipe_payload(ing["id"], "Banana Bread"))
    r = await client.get("/api/recipes?search=banana")
    names = [x["name"] for x in r.json()]
    assert "Banana Bread" in names
    assert "Apple Pie" not in names


# ── create ────────────────────────────────────────────────────────────────────

async def test_create_recipe_computes_nutrition(client: AsyncClient):
    ing = await _create_ingredient(client)
    r = await client.post("/api/recipes", json=_recipe_payload(ing["id"], servings=1))
    assert r.status_code == 201
    data = r.json()
    assert data["status"] == "complete"
    # 200g apple → 200/100 * 52 kcal = 104 kcal
    assert data["nutritionTotal"]["calories"] == pytest.approx(104.0, rel=0.01)
    assert data["nutritionPerServing"]["calories"] == pytest.approx(104.0, rel=0.01)


async def test_create_recipe_per_serving_divides_by_servings(client: AsyncClient):
    ing = await _create_ingredient(client)
    r = await client.post("/api/recipes", json=_recipe_payload(ing["id"], servings=4))
    data = r.json()
    assert data["nutritionPerServing"]["calories"] == pytest.approx(
        data["nutritionTotal"]["calories"] / 4, rel=0.01
    )


async def test_create_recipe_invalid_ingredient_returns_422(client: AsyncClient):
    r = await client.post(
        "/api/recipes",
        json={
            "name": "Bad Recipe",
            "servings": 1,
            "ingredients": [
                {
                    "ingredientId": "00000000-0000-0000-0000-000000000099",
                    "ingredientName": "Ghost",
                    "amount": 100,
                    "unit": "grams",
                }
            ],
            "cookInstructions": ["Cook it"],
            "prepTimeMinutes": 0,
            "cookTimeMinutes": 10,
        },
    )
    assert r.status_code == 422


async def test_import_recipe_from_url_body_creates_recipe_with_stub_ingredients(
    client: AsyncClient,
):
    payload = {
        "name": "Imported Ottolenghi Recipe",
        "description": "Imported from a URL",
        "servings": 4,
        "ingredients": [
            {
                "ingredientName": "Butter beans",
                "amount": 400,
                "unit": "grams",
            },
            {
                "ingredientName": "Calabrian chilli pesto",
                "amount": 240,
                "unit": "grams",
            },
        ],
        "cookInstructions": [
            "Mix the ingredients and roast until golden.",
        ],
        "prepTimeMinutes": 15,
        "cookTimeMinutes": 35,
        "source": "ottolenghi",
        "sourceUrl": "https://ottolenghi.co.uk/pages/recipes/roasted-aubergines-butter-beans-chilli-pesto",
    }

    r = await client.post("/api/recipes/import", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["name"] == "Imported Ottolenghi Recipe"
    assert data["status"] == "complete"
    assert data["source"] == "ottolenghi"
    assert len(data["ingredients"]) == 2
    assert data["ingredients"][0]["ingredientName"] == "Butter beans"
    assert data["ingredients"][1]["ingredientName"] == "Calabrian chilli pesto"


async def test_import_festive_hummus_recipe_from_url(client: AsyncClient):
    payload = {
        "name": "Festive hummus with roasted brussels sprouts and chestnuts",
        "description": "Ottolenghi festive hummus imported from URL.",
        "servings": 8,
        "ingredients": [
            {"ingredientName": "Olive oil", "amount": 120, "unit": "ml"},
            {"ingredientName": "Sage leaves", "amount": 10, "unit": "grams"},
            {"ingredientName": "Cooked chestnuts", "amount": 200, "unit": "grams"},
            {"ingredientName": "Brussels sprouts", "amount": 400, "unit": "grams"},
            {"ingredientName": "Lemon", "amount": 120, "unit": "grams"},
            {"ingredientName": "Cooked chickpeas", "amount": 500, "unit": "grams"},
            {"ingredientName": "Garlic cloves", "amount": 10, "unit": "grams"},
            {"ingredientName": "Ground cumin", "amount": 0.25, "unit": "tsp"},
            {"ingredientName": "Tahini", "amount": 120, "unit": "ml"},
            {"ingredientName": "White balsamic vinegar", "amount": 1, "unit": "tbsp"},
        ],
        "prepInstructions": [
            "Preheat the oven to 230°C.",
            "Heat oil in a tray and crisp the sage leaves, then remove them.",
        ],
        "cookInstructions": [
            "Roast the chestnuts, brussels sprouts, lemon zest, salt and pepper until charred.",
            "Blend chickpeas, garlic, water, cumin, tahini and lemon juice until smooth.",
            "Whisk olive oil, lemon juice and white balsamic into a dressing.",
            "Assemble hummus, top with roasted vegetables, sage and the dressing.",
        ],
        "prepTimeMinutes": 15,
        "cookTimeMinutes": 20,
        "source": "ottolenghi",
        "sourceUrl": "https://ottolenghi.co.uk/pages/recipes/festive-hummus-roasted-brussels-sprouts-chestnuts",
    }

    r = await client.post("/api/recipes/import", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["name"] == "Festive hummus with roasted brussels sprouts and chestnuts"
    assert data["status"] == "complete"
    assert data["source"] == "ottolenghi"
    assert data["sourceUrl"] == payload["sourceUrl"]
    assert len(data["ingredients"]) == 10


async def test_create_recipe_missing_servings_returns_422(client: AsyncClient):
    ing = await _create_ingredient(client)
    payload = _recipe_payload(ing["id"])
    del payload["servings"]
    r = await client.post("/api/recipes", json=payload)
    assert r.status_code == 422


# ── get ───────────────────────────────────────────────────────────────────────

async def test_get_recipe(client: AsyncClient):
    ing = await _create_ingredient(client)
    created = (await client.post("/api/recipes", json=_recipe_payload(ing["id"]))).json()
    r = await client.get(f"/api/recipes/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


async def test_get_recipe_not_found(client: AsyncClient):
    r = await client.get("/api/recipes/00000000-0000-0000-0000-000000000001")
    assert r.status_code == 404


# ── update ────────────────────────────────────────────────────────────────────

async def test_update_recipe_name(client: AsyncClient):
    ing = await _create_ingredient(client)
    created = (await client.post("/api/recipes", json=_recipe_payload(ing["id"]))).json()
    r = await client.put(f"/api/recipes/{created['id']}", json={"name": "New Name"})
    assert r.status_code == 200
    assert r.json()["name"] == "New Name"


async def test_update_recipe_recomputes_nutrition_on_servings_change(client: AsyncClient):
    ing = await _create_ingredient(client)
    created = (
        await client.post("/api/recipes", json=_recipe_payload(ing["id"], servings=2))
    ).json()
    original_per_serving = created["nutritionPerServing"]["calories"]

    r = await client.put(f"/api/recipes/{created['id']}", json={"servings": 4})
    new_per_serving = r.json()["nutritionPerServing"]["calories"]
    assert new_per_serving == pytest.approx(original_per_serving / 2, rel=0.01)


async def test_update_recipe_invalid_ingredient_returns_422(client: AsyncClient):
    ing = await _create_ingredient(client)
    created = (await client.post("/api/recipes", json=_recipe_payload(ing["id"]))).json()
    r = await client.put(
        f"/api/recipes/{created['id']}",
        json={
            "ingredients": [
                {
                    "ingredientId": "00000000-0000-0000-0000-000000000099",
                    "ingredientName": "Ghost",
                    "amount": 100,
                    "unit": "grams",
                }
            ]
        },
    )
    assert r.status_code == 422


# ── delete ────────────────────────────────────────────────────────────────────

async def test_delete_recipe(client: AsyncClient):
    ing = await _create_ingredient(client)
    created = (await client.post("/api/recipes", json=_recipe_payload(ing["id"]))).json()
    r = await client.delete(f"/api/recipes/{created['id']}")
    assert r.status_code == 204
    assert (await client.get(f"/api/recipes/{created['id']}")).status_code == 404


async def test_delete_recipe_clears_menu_slots(client: AsyncClient):
    ing = await _create_ingredient(client)
    recipe = (
        await client.post("/api/recipes", json=_recipe_payload(ing["id"]))
    ).json()

    menu_r = await client.post(
        "/api/menus",
        json={"name": "Week 1", "startDate": "2026-05-19", "endDate": "2026-05-25"},
    )
    menu = menu_r.json()

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

    await client.delete(f"/api/recipes/{recipe['id']}")

    updated_menu = (await client.get(f"/api/menus/{menu['id']}")).json()
    breakfast_ids = updated_menu["days"][0]["meals"]["breakfast"]
    assert recipe["id"] not in breakfast_ids


# ── preview ───────────────────────────────────────────────────────────────────

async def test_preview_nutrition(client: AsyncClient):
    ing = await _create_ingredient(client)
    r = await client.post(
        "/api/recipes/preview",
        json={
            "name": "Preview",
            "servings": 2,
            "ingredients": [
                {
                    "ingredientId": ing["id"],
                    "ingredientName": "Apple",
                    "amount": 200,
                    "unit": "grams",
                }
            ],
            "cookInstructions": ["Eat it"],
            "prepTimeMinutes": 0,
            "cookTimeMinutes": 0,
        },
    )
    assert r.status_code == 200
    data = r.json()
    # 200g / 2 servings = 100g per serving → 52 kcal
    assert data["nutritionPerServing"]["calories"] == pytest.approx(52.0, rel=0.01)
