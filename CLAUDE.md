# Noorish — CLAUDE.md

## Source of Truth

`docs/spec/spec.main.md` is the master spec. All implementation must align with it. **Update the spec before writing code that deviates from it.**

---

## Repo Layout

```
backend/
  app/
    config.py          pydantic-settings; reads .env
    database.py        SQLAlchemy async engine + session factory
    constants/dri.py   DRI reference values
    models/            SQLAlchemy ORM models (ingredient, recipe, menu, settings)
    schemas/           Pydantic request/response schemas (camelCase JSON)
    services/          Business logic (nutrition.py, ingest_usda.py, ingest_off.py)
  requirements.txt
  .env.example         → copy to .env; fill USDA_API_KEY
  alembic.ini

frontend/
  src/
    api/client.js      fetch wrapper; base URL /api
    hooks/             React Query hooks (useIngredients, useRecipes, useMenus, useSettings)
    components/        shadcn/ui + custom components
    views/             Page-level components
    lib/constants.js   shared enums/constants

docs/spec/spec.main.md  ← MASTER SPEC
```

---

## Dev Commands

**Backend** (from repo root):
```
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env            # fill in USDA_API_KEY
uvicorn app.main:app --reload --port 8000
```

**Frontend** (from repo root):
```
cd frontend
npm install
npm run dev                     # http://localhost:5173
```

**Database:** PostgreSQL at `localhost:5432`, db `noorish`, user `noorish` (see `.env.example`).

---

## Tech Stack

| Concern | Technology |
|---------|-----------|
| Backend | Python, FastAPI (async) |
| ORM | SQLAlchemy 2.0 async + asyncpg |
| Migrations | Alembic |
| Frontend | React 18, Vite |
| Styling | Tailwind CSS v3 + shadcn/ui |
| Server state | React Query v5 |
| Charts | Recharts |
| Drag & drop | @dnd-kit/core + @dnd-kit/sortable |
| Routing | React Router v6 |

---

## Conventions

- Backend code: `snake_case` (Python)
- API JSON (request/response): `camelCase`
- IDs: UUID v4
- Nutrition values: always stored and computed **per 100g**
- Dates: `YYYY-MM-DD` | Timestamps: UTC ISO 8601
- All API endpoints prefixed `/api`
- Color tokens: `color-main #E9E0D8`, `color-accent #C49450`, `color-green #79A486`, `color-dark #161f27`, `color-light #F7F8F8`

---

## Invariants (never violate)

1. `nutrition_total` / `nutrition_per_serving` on a Recipe are **computed by the backend on every create/update** — never set by the client.
2. Menu nutrition is **never stored** — computed on demand by `GET /api/menus/:id/nutrition`.
3. `recipe.status` is set by the backend only: `incomplete` when an `ingredient_id` reference is broken; `complete` otherwise.
4. Incomplete recipes cannot be added to menus.
5. Deleting an ingredient sets all referencing recipes to `incomplete`.
6. API keys live in `.env` only — never in source.

---

## Running Tests

Integration tests require PostgreSQL with a `noorish_test` database:
```sql
CREATE DATABASE noorish_test;
-- (same user/password as main DB — see .env.example)
```

```
cd backend
pip install -r requirements-dev.txt
pytest                        # all tests
pytest tests/test_nutrition_service.py  # unit tests only (no DB)
pytest -v                     # verbose
```

Set `TEST_DATABASE_URL` env var to override the default test DB URL.

---

## Phase 1 Scope

Full MVP across 5 feature groups: FR-1 Ingredient Management, FR-2 Recipe Builder, FR-3 Menu Planner, FR-4 Nutritional Analysis, FR-5 Grocery List. See spec §5 for the complete feature list.

Phases 2–4 are defined in the spec but not yet in scope.
