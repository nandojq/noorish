import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select, or_, String, cast
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings as app_settings
from app.database import get_db
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.schemas.ingredient import IngredientCreate, IngredientUpdate, IngredientResponse
from app.services import ingest_usda, ingest_off
from app.services.nutrition import compute_recipe_nutrition

router = APIRouter()


# ── request bodies for ingest endpoints ──────────────────────────────────────

class UsdaImportBody(BaseModel):
    fdcId: str
    overrides: Optional[dict] = None


class OffImportBody(BaseModel):
    offId: str
    overrides: Optional[dict] = None


# ── helpers ───────────────────────────────────────────────────────────────────

async def _rebuild_recipe_nutrition(recipe: Recipe, db: AsyncSession) -> None:
    ingredient_ids = [
        uuid.UUID(str(row.get("ingredient_id", "")))
        for row in recipe.ingredients
        if row.get("ingredient_id")
    ]
    result = await db.execute(
        select(Ingredient).where(Ingredient.id.in_(ingredient_ids))
    )
    db_ingredients = result.scalars().all()
    ingredient_map = {
        str(i.id): {
            "name": i.name,
            "nutrition_per_100g": i.nutrition_per_100g,
            "unit_weights": i.unit_weights,
            "density_g_per_ml": i.density_g_per_ml,
        }
        for i in db_ingredients
    }
    total, per_serving = compute_recipe_nutrition(
        recipe.ingredients, ingredient_map, recipe.servings
    )
    recipe.nutrition_total = total
    recipe.nutrition_per_serving = per_serving


async def _assert_name_available(
    name: str,
    db: AsyncSession,
    exclude_id: Optional[uuid.UUID] = None,
) -> None:
    stmt = select(Ingredient).where(Ingredient.name.ilike(name))
    if exclude_id is not None:
        stmt = stmt.where(Ingredient.id != exclude_id)
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=409,
            detail={"message": "Ingredient name already exists", "existingId": str(existing.id)},
        )


async def _persist_ingredient(data: dict, db: AsyncSession) -> Ingredient:
    await _assert_name_available(data["name"], db)
    ingredient = Ingredient(**data)
    db.add(ingredient)
    await db.flush()
    await db.refresh(ingredient)
    return ingredient


def _serialize_create(body: IngredientCreate) -> dict:
    return {
        "name": body.name,
        "aliases": body.aliases,
        "category": body.category,
        "season": body.season,
        "unit_weights": body.unit_weights.model_dump() if body.unit_weights else None,
        "density_g_per_ml": body.density_g_per_ml,
        "nutrition_per_100g": body.nutrition_per_100g.model_dump(),
        "environmental_impact": (
            body.environmental_impact.model_dump() if body.environmental_impact else None
        ),
        "ingredient_metadata": body.metadata.model_dump(),
    }


# ── ingredient CRUD ───────────────────────────────────────────────────────────

@router.get("/ingredients", response_model=list[IngredientResponse])
async def list_ingredients(
    search: Optional[str] = None,
    category: Optional[str] = None,
    data_quality: Optional[str] = Query(None, alias="dataQuality"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Ingredient).order_by(Ingredient.name)
    if search:
        stmt = stmt.where(
            or_(
                Ingredient.name.ilike(f"%{search}%"),
                cast(Ingredient.aliases, String).ilike(f"%{search}%"),
            )
        )
    if category:
        stmt = stmt.where(Ingredient.category == category)

    ingredients = (await db.execute(stmt)).scalars().all()

    # Filter data_quality in Python to avoid the `metadata` column name clash
    # with SQLAlchemy's DeclarativeBase.metadata at class level.
    if data_quality:
        ingredients = [
            i for i in ingredients
            if (i.ingredient_metadata or {}).get("data_quality") == data_quality
        ]

    return ingredients


@router.get("/ingredients/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(
    ingredient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    row = (
        await db.execute(select(Ingredient).where(Ingredient.id == ingredient_id))
    ).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail={"message": "Ingredient not found"})
    return row


@router.post("/ingredients", response_model=IngredientResponse, status_code=201)
async def create_ingredient(
    body: IngredientCreate,
    db: AsyncSession = Depends(get_db),
):
    return await _persist_ingredient(_serialize_create(body), db)


@router.put("/ingredients/{ingredient_id}", response_model=IngredientResponse)
async def update_ingredient(
    ingredient_id: uuid.UUID,
    body: IngredientUpdate,
    db: AsyncSession = Depends(get_db),
):
    row = (
        await db.execute(select(Ingredient).where(Ingredient.id == ingredient_id))
    ).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail={"message": "Ingredient not found"})

    if body.name is not None:
        await _assert_name_available(body.name, db, exclude_id=ingredient_id)
        row.name = body.name
    if body.aliases is not None:
        row.aliases = body.aliases
    if body.category is not None:
        row.category = body.category
    if body.season is not None:
        row.season = body.season
    if body.unit_weights is not None:
        row.unit_weights = body.unit_weights.model_dump()
    if body.density_g_per_ml is not None:
        row.density_g_per_ml = body.density_g_per_ml
    if body.environmental_impact is not None:
        row.environmental_impact = body.environmental_impact.model_dump()
    if body.metadata is not None:
        row.ingredient_metadata = body.metadata.model_dump()

    nutrition_changed = body.nutrition_per_100g is not None
    if nutrition_changed:
        row.nutrition_per_100g = body.nutrition_per_100g.model_dump()

    await db.flush()

    if nutrition_changed:
        affected = (
            await db.execute(
                select(Recipe).where(
                    Recipe.status == "complete",
                    Recipe.ingredients.contains([{"ingredient_id": str(ingredient_id)}]),
                )
            )
        ).scalars().all()
        for recipe in affected:
            await _rebuild_recipe_nutrition(recipe, db)

    await db.refresh(row)
    return row


@router.delete("/ingredients/{ingredient_id}", status_code=204)
async def delete_ingredient(
    ingredient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    row = (
        await db.execute(select(Ingredient).where(Ingredient.id == ingredient_id))
    ).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail={"message": "Ingredient not found"})

    affected = (
        await db.execute(
            select(Recipe).where(
                Recipe.ingredients.contains([{"ingredient_id": str(ingredient_id)}])
            )
        )
    ).scalars().all()
    for recipe in affected:
        recipe.status = "incomplete"

    await db.delete(row)


# ── USDA ingest ───────────────────────────────────────────────────────────────

@router.get("/ingest/usda/search")
async def search_usda_endpoint(q: str = Query(...)):
    if not app_settings.usda_api_key:
        raise HTTPException(status_code=500, detail={"message": "USDA API key not configured"})
    try:
        return await ingest_usda.search_usda(q, app_settings.usda_api_key)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail={"message": str(exc)})


@router.post("/ingest/usda/import", response_model=IngredientResponse, status_code=201)
async def import_usda_endpoint(
    body: UsdaImportBody,
    db: AsyncSession = Depends(get_db),
):
    if not app_settings.usda_api_key:
        raise HTTPException(status_code=500, detail={"message": "USDA API key not configured"})
    name_override = (body.overrides or {}).get("name")
    try:
        data = await ingest_usda.import_usda(body.fdcId, app_settings.usda_api_key, name_override)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail={"message": str(exc)})
    return await _persist_ingredient(data, db)


# ── Open Food Facts ingest ────────────────────────────────────────────────────

@router.get("/ingest/off/search")
async def search_off_endpoint(
    q: Optional[str] = None,
    barcode: Optional[str] = None,
):
    if q and barcode:
        raise HTTPException(
            status_code=400,
            detail={"message": "Provide either q or barcode, not both"},
        )
    if not q and not barcode:
        raise HTTPException(
            status_code=400,
            detail={"message": "Provide either q or barcode"},
        )
    try:
        if barcode:
            return await ingest_off.search_off_barcode(barcode)
        return await ingest_off.search_off(q)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail={"message": str(exc)})


@router.post("/ingest/off/import", response_model=IngredientResponse, status_code=201)
async def import_off_endpoint(
    body: OffImportBody,
    db: AsyncSession = Depends(get_db),
):
    name_override = (body.overrides or {}).get("name")
    try:
        data = await ingest_off.import_off(body.offId, name_override)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail={"message": str(exc)})
    return await _persist_ingredient(data, db)
