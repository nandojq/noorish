import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy import select
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
