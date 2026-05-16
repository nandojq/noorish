"""
Integration test configuration.

Requires a running PostgreSQL instance. Configure via TEST_DATABASE_URL env var
or use the default below.
"""
import os

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://noorish:noorish@localhost:5432/noorish_test",
)

_test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)
_TestSessionFactory = async_sessionmaker(
    bind=_test_engine, class_=AsyncSession, expire_on_commit=False
)


# ── session-scoped table setup ────────────────────────────────────────────────

@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables():
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await _test_engine.dispose()


# ── per-test cleanup ──────────────────────────────────────────────────────────

@pytest_asyncio.fixture(autouse=True)
async def clean_tables():
    """Truncate all tables before each test for a clean slate."""
    async with _TestSessionFactory() as session:
        table_names = ", ".join(
            f'"{t.name}"' for t in reversed(Base.metadata.sorted_tables)
        )
        await session.execute(text(f"TRUNCATE {table_names} RESTART IDENTITY CASCADE"))
        await session.commit()
    yield


# ── per-test client ───────────────────────────────────────────────────────────

@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async def _override_get_db():
        async with _TestSessionFactory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = _override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# ── shared fixture data ───────────────────────────────────────────────────────

MINIMAL_NUTRITION = {
    "calories": 52.0,
    "macronutrients": {
        "protein": 0.3,
        "carbohydrates": 13.8,
        "fat": 0.2,
        "fiber": 2.4,
        "sugar": 10.4,
        "saturated_fat": 0.0,
        "trans_fat": 0.0,
        "polyunsaturated_fat": 0.0,
        "monounsaturated_fat": 0.0,
        "added_sugars": 0.0,
        "cholesterol": 0.0,
    },
    "micronutrients": {
        "vitamins": {
            "vitamin_a": 3.0,
            "vitamin_c": 4.6,
            "vitamin_d": 0.0,
            "vitamin_e": 0.2,
            "vitamin_k": 2.2,
            "thiamine": 0.017,
            "riboflavin": 0.026,
            "niacin": 0.091,
            "vitamin_b6": 0.041,
            "folate": 3.0,
            "vitamin_b12": 0.0,
        },
        "minerals": {
            "calcium": 6.0,
            "iron": 0.12,
            "magnesium": 5.0,
            "phosphorus": 11.0,
            "potassium": 107.0,
            "zinc": 0.04,
            "copper": 0.027,
            "manganese": 0.035,
            "selenium": 0.0,
            "sodium": 1.0,
        },
    },
}

INGREDIENT_PAYLOAD = {
    "name": "Apple",
    "category": "fruit",
    "nutritionPer100G": MINIMAL_NUTRITION,
    "metadata": {
        "source": "manual",
        "lastUpdated": "2026-05-16T00:00:00Z",
        "dataQuality": "high",
    },
}
