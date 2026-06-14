import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy import select, or_, String, cast
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe, Image
from app.models.menu import Menu
from app.schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
    RecipeResponse,
    RecipeNutritionPreview,
)
from app.schemas.recipe_import import RecipeImportRequest
from app.services.nutrition import compute_recipe_nutrition

router = APIRouter()

_ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
_MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 MB


# ── helpers ───────────────────────────────────────────────────────────────────

async def _get_recipe_or_404(recipe_id: uuid.UUID, db: AsyncSession) -> Recipe:
    row = (
        await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    ).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail={"message": "Recipe not found"})
    return row


async def _fetch_ingredient_map(
    ingredient_rows: list[dict],
    db: AsyncSession,
) -> dict[str, dict]:
    ids = [uuid.UUID(str(r.get("ingredient_id", ""))) for r in ingredient_rows if r.get("ingredient_id")]
    if not ids:
        return {}
    result = await db.execute(select(Ingredient).where(Ingredient.id.in_(ids)))
    return {
        str(i.id): {
            "name": i.name,
            "nutrition_per_100g": i.nutrition_per_100g,
            "unit_weights": i.unit_weights,
            "density_g_per_ml": i.density_g_per_ml,
        }
        for i in result.scalars().all()
    }


async def _validate_ingredient_ids(
    ingredient_rows: list[dict],
    db: AsyncSession,
) -> dict[str, dict]:
    ingredient_map = await _fetch_ingredient_map(ingredient_rows, db)
    requested_ids = {str(r.get("ingredient_id", "")) for r in ingredient_rows if r.get("ingredient_id")}
    missing = requested_ids - ingredient_map.keys()
    if missing:
        raise HTTPException(
            status_code=422,
            detail={"message": f"Ingredient IDs not found: {', '.join(missing)}"},
        )
    return ingredient_map


async def _find_ingredient_by_name_or_alias(
    name: str,
    db: AsyncSession,
) -> Ingredient | None:
    stmt = select(Ingredient).where(
        or_(
            Ingredient.name.ilike(name),
            cast(Ingredient.aliases, String).ilike(f"%{name}%"),
        )
    )
    return (await db.execute(stmt)).scalars().first()


async def _create_stub_ingredient(
    name: str,
    db: AsyncSession,
) -> Ingredient:
    metadata = {
        "source": "imported",
        "source_id": None,
        "last_updated": datetime.utcnow().isoformat(),
        "data_quality": "low",
    }
    ingredient = Ingredient(
        name=name,
        aliases=[name],
        category="unknown",
        season=None,
        unit_weights=None,
        density_g_per_ml=None,
        nutrition_per_100g={
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
        },
        environmental_impact=None,
        ingredient_metadata=metadata,
    )
    db.add(ingredient)
    await db.flush()
    await db.refresh(ingredient)
    return ingredient


async def _resolve_import_ingredients(
    ingredient_rows: list[dict],
    db: AsyncSession,
) -> tuple[list[dict], dict[str, dict]]:
    resolved_rows = []
    ingredient_map: dict[str, dict] = {}

    for row in ingredient_rows:
        ingredient_id = row.get("ingredient_id")
        ingredient_name = row.get("ingredient_name")

        if ingredient_id:
            try:
                ingredient_id = str(uuid.UUID(str(ingredient_id)))
            except ValueError:
                raise HTTPException(
                    status_code=422,
                    detail={"message": f"Invalid ingredient ID: {ingredient_id}"},
                )
            result = await db.execute(select(Ingredient).where(Ingredient.id == ingredient_id))
            ingredient = result.scalars().first()
            if not ingredient:
                if not ingredient_name:
                    raise HTTPException(
                        status_code=422,
                        detail={"message": f"Ingredient ID not found: {ingredient_id}"},
                    )
                ingredient = await _create_stub_ingredient(ingredient_name, db)
        else:
            if not ingredient_name:
                raise HTTPException(
                    status_code=422,
                    detail={"message": "ingredientName is required when ingredientId is not provided"},
                )
            ingredient = await _find_ingredient_by_name_or_alias(ingredient_name, db)
            if not ingredient:
                ingredient = await _create_stub_ingredient(ingredient_name, db)

        resolved = {
            "ingredient_id": str(ingredient.id),
            "ingredient_name": ingredient.name,
            "amount": float(row.get("amount", 0)),
            "unit": row.get("unit", "grams"),
        }
        resolved_rows.append(resolved)
        ingredient_map[str(ingredient.id)] = {
            "name": ingredient.name,
            "nutrition_per_100g": ingredient.nutrition_per_100g,
            "unit_weights": ingredient.unit_weights,
            "density_g_per_ml": ingredient.density_g_per_ml,
        }

    return resolved_rows, ingredient_map


# ── endpoints ─────────────────────────────────────────────────────────────────

@router.get("/recipes", response_model=list[RecipeResponse])
async def list_recipes(
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Recipe).order_by(Recipe.name)
    if status:
        stmt = stmt.where(Recipe.status == status)
    if search:
        stmt = stmt.where(Recipe.name.ilike(f"%{search}%"))
    return (await db.execute(stmt)).scalars().all()


@router.post("/recipes/preview", response_model=RecipeNutritionPreview)
async def preview_recipe_nutrition(
    body: RecipeCreate,
    db: AsyncSession = Depends(get_db),
):
    rows = [r.model_dump(mode="json") for r in body.ingredients]
    ingredient_map = await _fetch_ingredient_map(rows, db)
    total, per_serving = compute_recipe_nutrition(rows, ingredient_map, body.servings)
    return RecipeNutritionPreview(nutrition_total=total, nutrition_per_serving=per_serving)


@router.post("/recipes/import", response_model=RecipeResponse, status_code=201)
async def import_recipe(
    body: RecipeImportRequest,
    db: AsyncSession = Depends(get_db),
):
    rows, ingredient_map = await _resolve_import_ingredients(
        [r.model_dump(mode="json") for r in body.ingredients],
        db,
    )

    total, per_serving = compute_recipe_nutrition(rows, ingredient_map, body.servings)

    recipe = Recipe(
        name=body.name,
        description=body.description,
        servings=body.servings,
        ingredients=rows,
        prep_instructions=body.prep_instructions,
        cook_instructions=body.cook_instructions,
        prep_time_minutes=body.prep_time_minutes,
        cook_time_minutes=body.cook_time_minutes,
        tags=body.tags,
        source=body.source or "imported",
        source_url=body.source_url,
        status="complete",
        nutrition_total=total,
        nutrition_per_serving=per_serving,
    )
    db.add(recipe)
    await db.flush()
    await db.refresh(recipe)
    return recipe


@router.get("/recipes/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await _get_recipe_or_404(recipe_id, db)


@router.post("/recipes", response_model=RecipeResponse, status_code=201)
async def create_recipe(body: RecipeCreate, db: AsyncSession = Depends(get_db)):
    rows = [r.model_dump(mode="json") for r in body.ingredients]
    ingredient_map = await _validate_ingredient_ids(rows, db)
    total, per_serving = compute_recipe_nutrition(rows, ingredient_map, body.servings)

    recipe = Recipe(
        name=body.name,
        description=body.description,
        servings=body.servings,
        ingredients=rows,
        prep_instructions=body.prep_instructions,
        cook_instructions=body.cook_instructions,
        prep_time_minutes=body.prep_time_minutes,
        cook_time_minutes=body.cook_time_minutes,
        tags=body.tags,
        source=body.source or "manual",
        source_url=body.source_url,
        status="complete",
        nutrition_total=total,
        nutrition_per_serving=per_serving,
    )
    db.add(recipe)
    await db.flush()
    await db.refresh(recipe)
    return recipe


@router.put("/recipes/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: uuid.UUID,
    body: RecipeUpdate,
    db: AsyncSession = Depends(get_db),
):
    recipe = await _get_recipe_or_404(recipe_id, db)

    if body.name is not None:
        recipe.name = body.name
    if body.description is not None:
        recipe.description = body.description
    if body.prep_instructions is not None:
        recipe.prep_instructions = body.prep_instructions
    if body.cook_instructions is not None:
        recipe.cook_instructions = body.cook_instructions
    if body.prep_time_minutes is not None:
        recipe.prep_time_minutes = body.prep_time_minutes
    if body.cook_time_minutes is not None:
        recipe.cook_time_minutes = body.cook_time_minutes
    if body.tags is not None:
        recipe.tags = body.tags
    if body.source is not None:
        recipe.source = body.source
    if body.source_url is not None:
        recipe.source_url = body.source_url

    recompute = False
    if body.servings is not None:
        recipe.servings = body.servings
        recompute = True
    if body.ingredients is not None:
        rows = [r.model_dump(mode="json") for r in body.ingredients]
        ingredient_map = await _validate_ingredient_ids(rows, db)
        recipe.ingredients = rows
        # If all ingredients are valid the recipe is complete
        recipe.status = "complete"
        recompute = True
    else:
        ingredient_map = None

    if recompute:
        if ingredient_map is None:
            ingredient_map = await _fetch_ingredient_map(recipe.ingredients, db)
        total, per_serving = compute_recipe_nutrition(
            recipe.ingredients, ingredient_map, recipe.servings
        )
        recipe.nutrition_total = total
        recipe.nutrition_per_serving = per_serving

    await db.flush()
    await db.refresh(recipe)
    return recipe


@router.delete("/recipes/{recipe_id}", status_code=204)
async def delete_recipe(recipe_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    recipe = await _get_recipe_or_404(recipe_id, db)

    # Delete associated image
    if recipe.image_id:
        image = (
            await db.execute(select(Image).where(Image.id == recipe.image_id))
        ).scalar_one_or_none()
        if image:
            await db.delete(image)

    # Clear this recipe from all menu slots
    recipe_id_str = str(recipe_id)
    all_menus = (await db.execute(select(Menu))).scalars().all()
    for menu in all_menus:
        updated_days = []
        changed = False
        for day in (menu.days or []):
            meals = day.get("meals", {})
            new_meals = {
                slot: [r for r in ids if str(r) != recipe_id_str]
                for slot, ids in meals.items()
            }
            if new_meals != meals:
                changed = True
            updated_days.append({**day, "meals": new_meals})
        if changed:
            menu.days = updated_days

    await db.delete(recipe)


# ── image endpoints ───────────────────────────────────────────────────────────

@router.get("/recipes/{recipe_id}/image")
async def get_recipe_image(recipe_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    recipe = await _get_recipe_or_404(recipe_id, db)
    if not recipe.image_id:
        raise HTTPException(status_code=404, detail={"message": "Recipe has no image"})

    image = (
        await db.execute(select(Image).where(Image.id == recipe.image_id))
    ).scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail={"message": "Image not found"})

    return Response(content=bytes(image.data), media_type=image.content_type)


@router.post("/recipes/{recipe_id}/image")
async def upload_recipe_image(
    recipe_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    recipe = await _get_recipe_or_404(recipe_id, db)

    if file.content_type not in _ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail={"message": f"Unsupported image type: {file.content_type}. Use JPEG, PNG, or WebP."},
        )

    data = await file.read()
    if len(data) > _MAX_IMAGE_BYTES:
        raise HTTPException(status_code=400, detail={"message": "Image exceeds 5 MB limit"})

    # Replace existing image if present
    if recipe.image_id:
        old_image = (
            await db.execute(select(Image).where(Image.id == recipe.image_id))
        ).scalar_one_or_none()
        if old_image:
            await db.delete(old_image)
            await db.flush()

    image = Image(data=data, content_type=file.content_type, recipe_id=recipe.id)
    db.add(image)
    await db.flush()

    recipe.image_id = image.id
    await db.flush()

    return {"imageId": str(image.id)}
