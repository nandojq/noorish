import uuid
from datetime import date as date_type
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.menu import Menu
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.settings import UserSettings
from app.schemas.menu import MenuCreate, MenuUpdate, MenuResponse, GroceryListResponse, GroceryItem
from app.schemas.nutrition import MenuNutritionAnalysis
from app.services.nutrition import compute_menu_nutrition_analysis, convert_to_grams

router = APIRouter()

_DEFAULT_SETTINGS = {
    "deficiency_threshold_percent_dv": 70,
    "excess_threshold_percent_dv": 150,
}


# ── helpers ───────────────────────────────────────────────────────────────────

async def _get_menu_or_404(menu_id: uuid.UUID, db: AsyncSession) -> Menu:
    row = (
        await db.execute(select(Menu).where(Menu.id == menu_id))
    ).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail={"message": "Menu not found"})
    return row


async def _get_analysis_settings(db: AsyncSession) -> dict:
    row = (
        await db.execute(select(UserSettings).where(UserSettings.id == 1))
    ).scalar_one_or_none()
    if row:
        return row.analysis or _DEFAULT_SETTINGS
    return _DEFAULT_SETTINGS


def _collect_recipe_ids(menu: Menu) -> set[str]:
    ids: set[str] = set()
    for day in (menu.days or []):
        for slot in ("breakfast", "lunch", "dinner", "snack"):
            for rid in (day.get("meals") or {}).get(slot) or []:
                ids.add(str(rid))
    return ids


def _count_recipe_occurrences(menu: Menu) -> dict[str, int]:
    counts: dict[str, int] = {}
    for day in (menu.days or []):
        for slot in ("breakfast", "lunch", "dinner", "snack"):
            for rid in (day.get("meals") or {}).get(slot) or []:
                key = str(rid)
                counts[key] = counts.get(key, 0) + 1
    return counts


# ── CRUD ──────────────────────────────────────────────────────────────────────

@router.get("/menus", response_model=list[MenuResponse])
async def list_menus(db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(Menu).order_by(Menu.start_date.desc()))).scalars().all()


@router.get("/menus/{menu_id}", response_model=MenuResponse)
async def get_menu(menu_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await _get_menu_or_404(menu_id, db)


@router.post("/menus", response_model=MenuResponse, status_code=201)
async def create_menu(body: MenuCreate, db: AsyncSession = Depends(get_db)):
    menu = Menu(
        name=body.name,
        start_date=body.start_date,
        end_date=body.end_date,
        days=[],
    )
    db.add(menu)
    await db.flush()
    await db.refresh(menu)
    return menu


@router.put("/menus/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: uuid.UUID,
    body: MenuUpdate,
    db: AsyncSession = Depends(get_db),
):
    menu = await _get_menu_or_404(menu_id, db)

    if body.name is not None:
        menu.name = body.name

    new_start = body.start_date or menu.start_date
    new_end = body.end_date or menu.end_date
    if new_end < new_start:
        raise HTTPException(
            status_code=400,
            detail={"message": "endDate must be >= startDate"},
        )
    menu.start_date = new_start
    menu.end_date = new_end

    if body.days is not None:
        # Validate: incomplete recipes cannot be assigned
        new_recipe_ids: set[str] = set()
        for day in body.days:
            for slot in ("breakfast", "lunch", "dinner", "snack"):
                for rid in getattr(day.meals, slot) or []:
                    new_recipe_ids.add(str(rid))

        if new_recipe_ids:
            result = await db.execute(
                select(Recipe.id, Recipe.status).where(
                    Recipe.id.in_([uuid.UUID(rid) for rid in new_recipe_ids])
                )
            )
            for recipe_id, status in result.all():
                if status == "incomplete":
                    raise HTTPException(
                        status_code=400,
                        detail={"message": f"Recipe {recipe_id} is incomplete and cannot be added to a menu"},
                    )

        # Validate all day dates are within range
        for day in body.days:
            day_date = date_type.fromisoformat(day.date)
            if not (new_start <= day_date <= new_end):
                raise HTTPException(
                    status_code=400,
                    detail={"message": f"Date {day.date} is outside the menu range"},
                )

        menu.days = [d.model_dump(mode="json") for d in body.days]

    await db.flush()
    await db.refresh(menu)
    return menu


@router.delete("/menus/{menu_id}", status_code=204)
async def delete_menu(menu_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    menu = await _get_menu_or_404(menu_id, db)
    await db.delete(menu)


# ── nutrition analysis ────────────────────────────────────────────────────────

@router.get("/menus/{menu_id}/nutrition", response_model=MenuNutritionAnalysis)
async def get_menu_nutrition(menu_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    menu = await _get_menu_or_404(menu_id, db)

    recipe_ids = _collect_recipe_ids(menu)
    if not recipe_ids:
        raise HTTPException(
            status_code=422,
            detail={"message": "Menu has no recipes assigned"},
        )

    recipes = (
        await db.execute(
            select(Recipe).where(Recipe.id.in_([uuid.UUID(rid) for rid in recipe_ids]))
        )
    ).scalars().all()

    recipe_map = {
        str(r.id): {"nutrition_total": r.nutrition_total or {}}
        for r in recipes
    }

    settings = await _get_analysis_settings(db)
    menu_dict = {"id": str(menu.id), "days": menu.days}

    return compute_menu_nutrition_analysis(menu_dict, recipe_map, settings)


# ── grocery list ──────────────────────────────────────────────────────────────

@router.get("/menus/{menu_id}/grocery-list", response_model=GroceryListResponse)
async def get_grocery_list(menu_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    menu = await _get_menu_or_404(menu_id, db)

    recipe_ids = _collect_recipe_ids(menu)
    if not recipe_ids:
        raise HTTPException(
            status_code=422,
            detail={"message": "Menu has no recipes assigned"},
        )

    recipes = (
        await db.execute(
            select(Recipe).where(Recipe.id.in_([uuid.UUID(rid) for rid in recipe_ids]))
        )
    ).scalars().all()

    # Collect all ingredient IDs referenced by the recipes
    all_ingredient_ids: set[str] = set()
    for recipe in recipes:
        for ri in recipe.ingredients:
            if ri.get("ingredient_id"):
                all_ingredient_ids.add(str(ri["ingredient_id"]))

    ingredient_rows = (
        await db.execute(
            select(Ingredient).where(
                Ingredient.id.in_([uuid.UUID(iid) for iid in all_ingredient_ids])
            )
        )
    ).scalars().all()
    ingredient_db_map = {str(i.id): i for i in ingredient_rows}

    # Count how many times each recipe appears across all menu slots
    recipe_counts = _count_recipe_occurrences(menu)

    # Aggregate ingredient quantities in grams
    totals: dict[str, dict] = {}
    for recipe in recipes:
        count = recipe_counts.get(str(recipe.id), 1)
        for ri in recipe.ingredients:
            iid = str(ri.get("ingredient_id", ""))
            ing = ingredient_db_map.get(iid)
            if not ing:
                continue

            amount = float(ri.get("amount", 0))
            unit = ri.get("unit", "grams")
            try:
                grams = convert_to_grams(
                    amount,
                    unit,
                    {
                        "name": ing.name,
                        "unit_weights": ing.unit_weights,
                        "density_g_per_ml": ing.density_g_per_ml,
                    },
                )
            except ValueError:
                grams = amount  # fallback: treat as grams

            grams *= count

            if iid not in totals:
                totals[iid] = {
                    "ingredient_id": uuid.UUID(iid),
                    "ingredient_name": ing.name,
                    "category": ing.category,
                    "total_grams": 0.0,
                }
            totals[iid]["total_grams"] += grams

    items = sorted(totals.values(), key=lambda x: (x["category"], x["ingredient_name"]))
    return GroceryListResponse(menu_id=menu_id, items=[GroceryItem(**i) for i in items])
