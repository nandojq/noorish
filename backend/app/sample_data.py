import datetime

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.services.nutrition import compute_recipe_nutrition

SAMPLE_INGREDIENTS = [
    {
        "name": "Garlic",
        "aliases": ["garlic clove"],
        "category": "herb_and_spice",
        "season": None,
        "unit_weights": {"small_unit_g": 3.0},
        "density_g_per_ml": None,
        "nutrition_per_100g": {
            "calories": 149.0,
            "macronutrients": {
                "protein": 6.36,
                "carbohydrates": 33.06,
                "fat": 0.5,
                "fiber": 2.1,
                "sugar": 1.0,
                "saturated_fat": 0.1,
            },
            "micronutrients": {
                "vitamins": {
                    "vitamin_c": 31.2,
                },
                "minerals": {
                    "calcium": 181.0,
                    "iron": 1.7,
                    "potassium": 401.0,
                },
            },
        },
        "ingredient_metadata": {
            "source": "manual",
            "source_id": None,
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "data_quality": "medium",
        },
    },
    {
        "name": "Onion",
        "aliases": ["yellow onion"],
        "category": "vegetable",
        "season": None,
        "unit_weights": None,
        "density_g_per_ml": None,
        "nutrition_per_100g": {
            "calories": 40.0,
            "macronutrients": {
                "protein": 1.1,
                "carbohydrates": 9.34,
                "fat": 0.1,
                "fiber": 1.7,
                "sugar": 4.24,
                "saturated_fat": 0.0,
            },
            "micronutrients": {
                "vitamins": {
                    "vitamin_c": 7.4,
                },
                "minerals": {
                    "calcium": 23.0,
                    "iron": 0.21,
                    "potassium": 146.0,
                },
            },
        },
        "ingredient_metadata": {
            "source": "manual",
            "source_id": None,
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "data_quality": "medium",
        },
    },
    {
        "name": "Aubergine",
        "aliases": ["eggplant"],
        "category": "vegetable",
        "season": None,
        "unit_weights": None,
        "density_g_per_ml": None,
        "nutrition_per_100g": {
            "calories": 25.0,
            "macronutrients": {
                "protein": 1.0,
                "carbohydrates": 5.88,
                "fat": 0.18,
                "fiber": 3.0,
                "sugar": 3.5,
                "saturated_fat": 0.0,
            },
            "micronutrients": {
                "vitamins": {
                    "vitamin_c": 2.2,
                },
                "minerals": {
                    "calcium": 9.0,
                    "iron": 0.23,
                    "potassium": 229.0,
                },
            },
        },
        "ingredient_metadata": {
            "source": "manual",
            "source_id": None,
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "data_quality": "medium",
        },
    },
    {
        "name": "Olive oil",
        "aliases": ["extra virgin olive oil"],
        "category": "fat_and_oil",
        "season": None,
        "unit_weights": None,
        "density_g_per_ml": 0.91,
        "nutrition_per_100g": {
            "calories": 884.0,
            "macronutrients": {
                "protein": 0.0,
                "carbohydrates": 0.0,
                "fat": 100.0,
                "fiber": 0.0,
                "sugar": 0.0,
                "saturated_fat": 14.0,
                "monounsaturated_fat": 73.0,
                "polyunsaturated_fat": 11.0,
            },
            "micronutrients": {
                "vitamins": {
                    "vitamin_e": 14.35,
                    "vitamin_k": 60.0,
                },
                "minerals": {},
            },
        },
        "ingredient_metadata": {
            "source": "manual",
            "source_id": None,
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "data_quality": "medium",
        },
    },
    {
        "name": "Butter beans",
        "aliases": ["lima beans"],
        "category": "protein",
        "season": None,
        "unit_weights": None,
        "density_g_per_ml": None,
        "nutrition_per_100g": {
            "calories": 120.0,
            "macronutrients": {
                "protein": 7.0,
                "carbohydrates": 20.0,
                "fat": 0.5,
                "fiber": 6.6,
                "sugar": 1.9,
                "saturated_fat": 0.1,
            },
            "micronutrients": {
                "vitamins": {},
                "minerals": {
                    "iron": 1.8,
                    "calcium": 35.0,
                    "potassium": 320.0,
                },
            },
        },
        "ingredient_metadata": {
            "source": "manual",
            "source_id": None,
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "data_quality": "medium",
        },
    },
    {
        "name": "Calabrian chilli pesto",
        "aliases": ["chilli pesto"],
        "category": "condiment_and_sauce",
        "season": None,
        "unit_weights": None,
        "density_g_per_ml": None,
        "nutrition_per_100g": {
            "calories": 370.0,
            "macronutrients": {
                "protein": 5.0,
                "carbohydrates": 8.0,
                "fat": 33.0,
                "fiber": 2.0,
                "sugar": 4.0,
                "saturated_fat": 5.0,
            },
            "micronutrients": {
                "vitamins": {},
                "minerals": {
                    "sodium": 800.0,
                },
            },
        },
        "ingredient_metadata": {
            "source": "manual",
            "source_id": None,
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "data_quality": "low",
        },
    },
    {
        "name": "Plum cherry tomatoes",
        "aliases": ["cherry tomatoes", "plum tomatoes"],
        "category": "vegetable",
        "season": None,
        "unit_weights": None,
        "density_g_per_ml": None,
        "nutrition_per_100g": {
            "calories": 18.0,
            "macronutrients": {
                "protein": 0.9,
                "carbohydrates": 3.9,
                "fat": 0.2,
                "fiber": 1.2,
                "sugar": 2.6,
                "saturated_fat": 0.0,
            },
            "micronutrients": {
                "vitamins": {
                    "vitamin_c": 18.0,
                },
                "minerals": {
                    "potassium": 237.0,
                },
            },
        },
        "ingredient_metadata": {
            "source": "manual",
            "source_id": None,
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "data_quality": "medium",
        },
    },
]

SAMPLE_RECIPE = {
    "name": "Roasted aubergines and butter beans in chilli pesto",
    "description": (
        "A simple Ottolenghi-inspired one-pan recipe with roast aubergine, butter beans, "
        "chilli pesto and cherry tomatoes. Serve with yoghurt and coriander if you like."
    ),
    "servings": 4,
    "prep_instructions": [
        "Preheat the oven to 230°C.",
        "Toss the garlic, onion, aubergine, half the olive oil, 1/4 teaspoon of salt and a good grind of black pepper in a 30cm shallow roasting pan.",
        "Roast for 20 minutes until golden and softened.",
        "Mix the remaining oil with the butter beans, chilli pesto, tomatoes and 1/4 teaspoon of salt, then spoon the mixture over the aubergines.",
        "Roast for a further 15 minutes until the butter beans are golden in places.",
        "Serve with yoghurt and coriander leaves if using."
    ],
    "cook_instructions": [
        "Use a hot oven so the aubergines caramelise and the butter beans get a little charred.",
        "This dish is perfect with flatbreads or rice for scooping up the sauce."
    ],
    "prep_time_minutes": 15,
    "cook_time_minutes": 35,
    "tags": ["vegetarian", "easy", "dinner"],
    "source": "ottolenghi",
    "source_url": "https://ottolenghi.co.uk/pages/recipes/roasted-aubergines-butter-beans-chilli-pesto",
}


async def _get_or_create_ingredient(session, ingredient_data):
    existing = (
        await session.execute(select(Ingredient).where(Ingredient.name == ingredient_data["name"]))
    ).scalar_one_or_none()
    if existing:
        return existing

    ingredient = Ingredient(**ingredient_data)
    session.add(ingredient)
    await session.flush()
    return ingredient


async def seed_sample_recipe():
    async with AsyncSessionLocal() as session:
        try:
            existing = (
                await session.execute(select(Recipe).where(Recipe.name == SAMPLE_RECIPE["name"]))
            ).scalar_one_or_none()
            if existing:
                return

            ingredients = []
            for ingredient_data in SAMPLE_INGREDIENTS:
                ingredient = await _get_or_create_ingredient(session, ingredient_data)
                ingredients.append(ingredient)

            ingredient_map = {str(i.id): {
                "name": i.name,
                "nutrition_per_100g": i.nutrition_per_100g,
                "unit_weights": i.unit_weights,
                "density_g_per_ml": i.density_g_per_ml,
            } for i in ingredients}

            recipe_ingredients = [
                {
                    "ingredient_id": str(next(i.id for i in ingredients if i.name == "Garlic")),
                    "ingredient_name": "Garlic",
                    "amount": 5.0,
                    "unit": "small_unit",
                },
                {
                    "ingredient_id": str(next(i.id for i in ingredients if i.name == "Onion")),
                    "ingredient_name": "Onion",
                    "amount": 360.0,
                    "unit": "grams",
                },
                {
                    "ingredient_id": str(next(i.id for i in ingredients if i.name == "Aubergine")),
                    "ingredient_name": "Aubergine",
                    "amount": 400.0,
                    "unit": "grams",
                },
                {
                    "ingredient_id": str(next(i.id for i in ingredients if i.name == "Olive oil")),
                    "ingredient_name": "Olive oil",
                    "amount": 120.0,
                    "unit": "ml",
                },
                {
                    "ingredient_id": str(next(i.id for i in ingredients if i.name == "Butter beans")),
                    "ingredient_name": "Butter beans",
                    "amount": 400.0,
                    "unit": "grams",
                },
                {
                    "ingredient_id": str(next(i.id for i in ingredients if i.name == "Calabrian chilli pesto")),
                    "ingredient_name": "Calabrian chilli pesto",
                    "amount": 240.0,
                    "unit": "grams",
                },
                {
                    "ingredient_id": str(next(i.id for i in ingredients if i.name == "Plum cherry tomatoes")),
                    "ingredient_name": "Plum cherry tomatoes",
                    "amount": 240.0,
                    "unit": "grams",
                },
            ]

            total, per_serving = compute_recipe_nutrition(recipe_ingredients, ingredient_map, SAMPLE_RECIPE["servings"])

            recipe = Recipe(
                name=SAMPLE_RECIPE["name"],
                description=SAMPLE_RECIPE["description"],
                servings=SAMPLE_RECIPE["servings"],
                ingredients=recipe_ingredients,
                prep_instructions=SAMPLE_RECIPE["prep_instructions"],
                cook_instructions=SAMPLE_RECIPE["cook_instructions"],
                prep_time_minutes=SAMPLE_RECIPE["prep_time_minutes"],
                cook_time_minutes=SAMPLE_RECIPE["cook_time_minutes"],
                tags=SAMPLE_RECIPE["tags"],
                source=SAMPLE_RECIPE["source"],
                source_url=SAMPLE_RECIPE["source_url"],
                status="complete",
                nutrition_total=total,
                nutrition_per_serving=per_serving,
            )
            session.add(recipe)
            await session.commit()
        except Exception:
            await session.rollback()
            raise
