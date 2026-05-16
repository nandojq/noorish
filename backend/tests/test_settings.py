"""Integration tests for /api/settings endpoints."""
from httpx import AsyncClient


async def test_get_settings_returns_defaults(client: AsyncClient):
    r = await client.get("/api/settings")
    assert r.status_code == 200
    data = r.json()
    assert data["analysis"]["deficiencyThresholdPercentDv"] == 70
    assert data["analysis"]["excessThresholdPercentDv"] == 150


async def test_update_settings(client: AsyncClient):
    r = await client.put(
        "/api/settings",
        json={"analysis": {"deficiencyThresholdPercentDv": 60, "excessThresholdPercentDv": 200}},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["analysis"]["deficiencyThresholdPercentDv"] == 60
    assert data["analysis"]["excessThresholdPercentDv"] == 200


async def test_updated_settings_persisted(client: AsyncClient):
    await client.put(
        "/api/settings",
        json={"analysis": {"deficiencyThresholdPercentDv": 55, "excessThresholdPercentDv": 180}},
    )
    r = await client.get("/api/settings")
    assert r.json()["analysis"]["deficiencyThresholdPercentDv"] == 55


async def test_update_settings_idempotent(client: AsyncClient):
    payload = {"analysis": {"deficiencyThresholdPercentDv": 65, "excessThresholdPercentDv": 160}}
    await client.put("/api/settings", json=payload)
    await client.put("/api/settings", json=payload)
    r = await client.get("/api/settings")
    assert r.json()["analysis"]["deficiencyThresholdPercentDv"] == 65


async def test_update_settings_invalid_deficiency_too_high(client: AsyncClient):
    r = await client.put(
        "/api/settings",
        json={"analysis": {"deficiencyThresholdPercentDv": 100, "excessThresholdPercentDv": 150}},
    )
    assert r.status_code == 422


async def test_update_settings_invalid_excess_too_low(client: AsyncClient):
    r = await client.put(
        "/api/settings",
        json={"analysis": {"deficiencyThresholdPercentDv": 70, "excessThresholdPercentDv": 100}},
    )
    assert r.status_code == 422


async def test_update_settings_no_body_returns_current(client: AsyncClient):
    await client.put(
        "/api/settings",
        json={"analysis": {"deficiencyThresholdPercentDv": 65, "excessThresholdPercentDv": 160}},
    )
    r = await client.put("/api/settings", json={})
    assert r.status_code == 200
    assert r.json()["analysis"]["deficiencyThresholdPercentDv"] == 65
