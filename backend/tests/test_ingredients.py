"""Integration tests for /api/ingredients and /api/ingest/* endpoints."""
import pytest
from httpx import AsyncClient

from tests.conftest import INGREDIENT_PAYLOAD, MINIMAL_NUTRITION


async def _create_ingredient(client: AsyncClient, overrides: dict | None = None) -> dict:
    payload = {**INGREDIENT_PAYLOAD, **(overrides or {})}
    r = await client.post("/api/ingredients", json=payload)
    assert r.status_code == 201, r.text
    return r.json()


# ── list ──────────────────────────────────────────────────────────────────────

async def test_list_empty(client: AsyncClient):
    r = await client.get("/api/ingredients")
    assert r.status_code == 200
    assert r.json() == []


async def test_list_returns_created(client: AsyncClient):
    await _create_ingredient(client)
    r = await client.get("/api/ingredients")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["name"] == "Apple"


async def test_list_search_by_name(client: AsyncClient):
    await _create_ingredient(client, {"name": "Apple"})
    await _create_ingredient(client, {"name": "Banana"})
    r = await client.get("/api/ingredients?search=ban")
    assert r.status_code == 200
    names = [i["name"] for i in r.json()]
    assert "Banana" in names
    assert "Apple" not in names


async def test_list_filter_by_category(client: AsyncClient):
    await _create_ingredient(client, {"name": "Apple", "category": "fruit"})
    await _create_ingredient(client, {"name": "Chicken", "category": "protein"})
    r = await client.get("/api/ingredients?category=protein")
    assert r.status_code == 200
    assert all(i["category"] == "protein" for i in r.json())


async def test_list_filter_by_data_quality(client: AsyncClient):
    await _create_ingredient(
        client,
        {
            "name": "Apple",
            "metadata": {
                "source": "manual",
                "lastUpdated": "2026-05-16T00:00:00Z",
                "dataQuality": "high",
            },
        },
    )
    await _create_ingredient(
        client,
        {
            "name": "Banana",
            "metadata": {
                "source": "manual",
                "lastUpdated": "2026-05-16T00:00:00Z",
                "dataQuality": "medium",
            },
        },
    )
    r = await client.get("/api/ingredients?dataQuality=high")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["name"] == "Apple"


# ── get single ────────────────────────────────────────────────────────────────

async def test_get_ingredient(client: AsyncClient):
    created = await _create_ingredient(client)
    r = await client.get(f"/api/ingredients/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


async def test_get_ingredient_not_found(client: AsyncClient):
    r = await client.get("/api/ingredients/00000000-0000-0000-0000-000000000001")
    assert r.status_code == 404


# ── create ────────────────────────────────────────────────────────────────────

async def test_create_ingredient_returns_id(client: AsyncClient):
    r = await client.post("/api/ingredients", json=INGREDIENT_PAYLOAD)
    assert r.status_code == 201
    data = r.json()
    assert "id" in data
    assert data["name"] == "Apple"
    assert data["category"] == "fruit"


async def test_create_ingredient_duplicate_name_returns_409(client: AsyncClient):
    await _create_ingredient(client)
    r = await client.post("/api/ingredients", json=INGREDIENT_PAYLOAD)
    assert r.status_code == 409
    assert "existingId" in r.json()["detail"]


async def test_create_ingredient_missing_required_field(client: AsyncClient):
    payload = {k: v for k, v in INGREDIENT_PAYLOAD.items() if k != "name"}
    r = await client.post("/api/ingredients", json=payload)
    assert r.status_code == 422


# ── update ────────────────────────────────────────────────────────────────────

async def test_update_ingredient_name(client: AsyncClient):
    created = await _create_ingredient(client)
    r = await client.put(
        f"/api/ingredients/{created['id']}", json={"name": "Green Apple"}
    )
    assert r.status_code == 200
    assert r.json()["name"] == "Green Apple"


async def test_update_ingredient_not_found(client: AsyncClient):
    r = await client.put(
        "/api/ingredients/00000000-0000-0000-0000-000000000001",
        json={"name": "X"},
    )
    assert r.status_code == 404


async def test_update_ingredient_duplicate_name_returns_409(client: AsyncClient):
    a = await _create_ingredient(client, {"name": "Apple"})
    await _create_ingredient(client, {"name": "Banana"})
    r = await client.put(f"/api/ingredients/{a['id']}", json={"name": "Banana"})
    assert r.status_code == 409


# ── delete ────────────────────────────────────────────────────────────────────

async def test_delete_ingredient(client: AsyncClient):
    created = await _create_ingredient(client)
    r = await client.delete(f"/api/ingredients/{created['id']}")
    assert r.status_code == 204
    r2 = await client.get(f"/api/ingredients/{created['id']}")
    assert r2.status_code == 404


async def test_delete_ingredient_not_found(client: AsyncClient):
    r = await client.delete("/api/ingredients/00000000-0000-0000-0000-000000000001")
    assert r.status_code == 404


async def test_delete_ingredient_marks_recipes_incomplete(client: AsyncClient):
    ing = await _create_ingredient(client)
    recipe_payload = {
        "name": "Apple Salad",
        "servings": 2,
        "ingredients": [
            {
                "ingredientId": ing["id"],
                "ingredientName": "Apple",
                "amount": 100,
                "unit": "grams",
            }
        ],
        "cookInstructions": ["Mix everything"],
        "prepTimeMinutes": 5,
        "cookTimeMinutes": 0,
    }
    recipe_r = await client.post("/api/recipes", json=recipe_payload)
    assert recipe_r.status_code == 201
    recipe_id = recipe_r.json()["id"]

    await client.delete(f"/api/ingredients/{ing['id']}")

    r = await client.get(f"/api/recipes/{recipe_id}")
    assert r.json()["status"] == "incomplete"
