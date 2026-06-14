# Noorish

A personal nutrition planning tool for building weekly menus, tracking nutrient intake, and generating grocery lists. Built as a local-first web app with a FastAPI backend and React frontend.

---

## Features

- **Ingredient Database** — Import ingredients from USDA FoodData Central or Open Food Facts, or add them manually with full nutrition data
- **Recipe Builder** — Compose recipes from ingredients with live nutrition preview, prep/cook instructions, and image upload
- **Menu Planner** — Drag-and-drop weekly planner assigning recipes to breakfast, lunch, dinner, and snack slots
- **Nutrition Analysis** — Per-day and weekly-average breakdown with DRI (Daily Reference Intake) comparison and configurable deficiency/excess thresholds
- **Grocery List** — Auto-generated shopping list aggregated from all recipes in a menu, exportable as TXT or CSV

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12+, FastAPI (async) |
| ORM | SQLAlchemy 2.0 async + asyncpg |
| Migrations | Alembic |
| Database | PostgreSQL 15+ |
| Frontend | React 18, Vite |
| Styling | Tailwind CSS v3, neumorphic design system |
| Server state | React Query v5 |
| Charts | Recharts |
| Drag & drop | @dnd-kit/core |
| Routing | React Router v6 |
| Nutrition data | USDA FoodData Central API, Open Food Facts |

---

## Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 15+ running locally (or via Docker)

---

## Setup

### 1. Database

Create the database and user in PostgreSQL:

```sql
CREATE USER noorish WITH PASSWORD 'noorish';
CREATE DATABASE noorish OWNER noorish;
CREATE DATABASE noorish_test OWNER noorish;  -- for tests only
```

Or with Docker:

```bash
docker compose up -d
```

### 2. Backend

```bash
cd backend
python -m venv .venv

# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set USDA_API_KEY (optional — only needed for USDA import)

# Run migrations
alembic upgrade head
```

### 3. Frontend

```bash
cd frontend
npm install
```

---

## Running

### One command (Windows)

```powershell
.\start.ps1
```

This script starts Postgres via Docker, waits for it to be healthy, runs any pending migrations, then launches the backend and frontend. Press **Ctrl+C** to stop everything cleanly.

Requires Docker Desktop to be running. On first run, complete the [Setup](#setup) steps below first.

### Manually (two terminals)

**Terminal 1 — Backend:**
```bash
cd backend
.\.venv\Scripts\activate      # Windows
# source .venv/bin/activate   # macOS / Linux
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser. The backend API is available at **http://localhost:8000/api**.

---

## Importing Recipes from URL

The backend exposes a reusable import endpoint for AI-assisted recipe creation:

- `POST /api/recipes/import`
- Request body must follow the `RecipeImportRequest` schema
- Each ingredient may include either `ingredientId` or `ingredientName`
- Missing ingredient matches create low-quality stub ingredients automatically

Example payload:

```json
{
  "name": "Roasted Aubergines with Butter Beans & Chilli Pesto",
  "description": "A bulk-style recipe imported from a URL.",
  "servings": 4,
  "ingredients": [
    {"ingredientName": "Large aubergines", "amount": 2, "unit": "pieces"},
    {"ingredientName": "Butter beans", "amount": 400, "unit": "grams"},
    {"ingredientName": "Calabrian chilli pesto", "amount": 240, "unit": "grams"}
  ],
  "prepInstructions": ["Preheat oven.", "Slice aubergines and season.", "Roast until tender."],
  "cookInstructions": ["Mix with beans and pesto.", "Serve warm."],
  "prepTimeMinutes": 15,
  "cookTimeMinutes": 35,
  "source": "ottolenghi",
  "sourceUrl": "https://ottolenghi.co.uk/pages/recipes/roasted-aubergines-butter-beans-chilli-pesto"
}
```

The import endpoint returns the created recipe with nutrition computed by the backend.

---

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in:

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://noorish:noorish@localhost:5432/noorish` |
| `USDA_API_KEY` | API key from [api.nal.usda.gov](https://api.nal.usda.gov) | *(empty — USDA import disabled)* |
| `CORS_ORIGINS` | Allowed frontend origins (JSON array) | `["http://localhost:5173"]` |

---

## Running Tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest            # all tests
pytest -v         # verbose
pytest tests/test_nutrition_service.py   # unit tests only (no DB required)
```

Tests require the `noorish_test` database to exist (see Setup above).

---

## Project Structure

```
backend/
  app/
    config.py          Environment / settings (pydantic-settings)
    database.py        SQLAlchemy async engine and session
    constants/dri.py   Daily Reference Intake values
    models/            ORM models (ingredient, recipe, menu, settings)
    routers/           FastAPI route handlers
    schemas/           Pydantic request/response schemas
    services/          Business logic (nutrition, USDA ingest, OFF ingest)
  alembic/             Database migrations
  tests/
  requirements.txt
  .env.example

frontend/
  src/
    api/client.js      Fetch wrapper (base URL /api)
    hooks/             React Query hooks
    components/        Shared UI components
    views/             Page-level components
    lib/constants.js   Shared enums and constants

docs/spec/spec.main.md   Master feature specification
```

---

## License

MIT
