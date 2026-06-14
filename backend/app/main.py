from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import ingredients, recipes, menus
from app.routers import settings as settings_router
from app.sample_data import seed_sample_recipe

app = FastAPI(title="Noorish API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingredients.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")
app.include_router(menus.router, prefix="/api")
app.include_router(settings_router.router, prefix="/api")


@app.on_event("startup")
async def on_startup():
    try:
        await seed_sample_recipe()
    except Exception:
        # Failures during sample seeding should not prevent the API from starting.
        pass
