# Noorish — Master Specification

> **This document is the single source of truth for all Noorish development.**
> All code changes must align with it. Update this document before implementing any change that diverges from it.

---

## 1. Project Overview

### 1.1 Vision

Noorish is a personal nutrition analysis framework. It ingests ingredient data from external APIs, standardises it into a local database, and enables recipe and menu-level nutritional analysis.

Not a commercial product: a research and coding exploration with potential to grow into a lightweight web app for a small community.

### 1.2 Done Means

A user can:
- Plan a full week of meals by assigning recipes to dates and meal types
- Get a complete nutritional breakdown (macros + micros) for any recipe or menu
- Identify nutritional deficiencies against DRI standards

### 1.3 Scope Boundaries

**In scope:**
- Ingredient database management (import from USDA and Open Food Facts, manual creation)
- Recipe creation and nutritional analysis
- Weekly menu planning and nutritional totals
- DRI-based deficiency analysis
- Grocery list generation from active menu
- Grocery procurement agent with price comparison and ordering (Phase 4)

**Out of scope:**
- Calorie tracking / food diary (this is planning, not logging)
- Medical or clinical dietary advice
- Commercial features (payment, subscriptions)

---

## 2. System Architecture

### 2.1 Architecture Overview

```
[ External APIs ]
USDA FoodData Central, Open Food Facts
(manually triggered by user)
          ↓
┌──────────────────────────────────────┐
│             BACKEND                  │
│  FastAPI — Python                    │
│  • Ingest: query, normalise, store   │
│  • Calculate: nutrition, DRI, lists  │
│  • Serve: REST API for frontend      │
├──────────────────────────────────────┤
│  Database — PostgreSQL               │
│  ingredients, recipes, menus         │
└──────────────────────────────────────┘
          ↕  REST API
┌──────────────────────────────────────┐
│             FRONTEND                 │
│  React SPA                           │
│  • Ingredient browser + ingest UI    │
│  • Recipe builder and viewer         │
│  • Weekly menu planner               │
│  • Nutrition visualisation           │
│  • Grocery list                      │
└──────────────────────────────────────┘
```

### 2.2 Backend Modules

| Module | Responsibility |
|--------|---------------|
| `ingest` | Query USDA and Open Food Facts; normalise; validate; persist to database |
| `recipes` | Recipe CRUD; per-serving and total nutrition calculation |
| `menus` | Menu CRUD; daily and weekly nutrition totals |
| `analyse` | DRI comparison; deficiency and excess flagging; summary generation |
| `grocery` | Derive shopping list from menu; aggregate ingredient quantities across all recipes |
| `api` | REST API layer — exposes all backend functionality to the frontend |
| `config` | API keys, DRI constants, application settings |

### 2.3 Frontend Views

| View | Responsibility |
|------|---------------|
| Ingredients | Browse and search the ingredient database; trigger manual ingest from APIs |
| Recipes | Create, edit, duplicate, and view recipes with full nutrition breakdown |
| Menu | Build weekly meal plan by assigning recipes; view per-day and weekly nutrition |
| Analysis | DRI comparison chart; deficiency and excess highlights |
| Grocery | Review aggregated shopping list from active menu; export |

**Frontend requirements:** Responsive across desktop and tablet. Intuitive — core actions reachable in ≤ 2 steps. Stylish — consistent design system using Tailwind CSS + shadcn/ui components.

---

## 3. Tech Stack

| Concern | Decision | Status |
|---------|----------|--------|
| Backend language | Python | Confirmed |
| Backend framework | FastAPI | Confirmed |
| Frontend framework | React + Vite | Confirmed |
| UI styling | Tailwind CSS + shadcn/ui | Confirmed |
| Database | PostgreSQL | Confirmed |
| Ingest APIs | USDA FoodData Central, Open Food Facts | Confirmed |
| DRI standard | Universal 2000 kcal adult baseline | Confirmed |

> **Why FastAPI over Java/Spring Boot:** Python is the existing project language; FastAPI is async-native and benchmarks comparably to Node.js for I/O-bound workloads; minimal boilerplate for a personal project. Spring Boot is a valid alternative but would require abandoning the existing Python codebase.

> **Why PostgreSQL over JSON/SQLite:** A web app with a backend API requires a proper relational database. PostgreSQL handles the ingredient/recipe/menu relationships cleanly and is production-ready from day one.

---

## 4. Data Models

**Conventions:**
- All field names: `snake_case`
- All IDs: UUID v4
- Dates: `YYYY-MM-DD` (ISO 8601)
- Timestamps: `YYYY-MM-DDTHH:MM:SSZ` (UTC)
- Nutrition values are always stored and computed **per 100g**
- All data persisted in PostgreSQL; these schemas define the logical structure, not table DDL

---

### 4.1 Ingredient

Represents a single food product with full nutritional data.

```json
{
  "id": "uuid-v4",
  "name": "string",
  "aliases": ["string"],
  "category": "protein | vegetable | grain_and_cereal | fruit | dairy | fat_and_oil | condiment_and_sauce | herb_and_spice | beverage | snack",
  "season": "all_year | winter | spring | summer | autumn",
  "unit_weights": {
    "small_unit_g":  "number — optional: grams per small unit (e.g. small egg ≈ 44g)",
    "medium_unit_g": "number — optional: grams per medium unit (e.g. medium egg ≈ 50g)",
    "large_unit_g":  "number — optional: grams per large unit (e.g. large egg ≈ 56g)"
  },
  "density_g_per_ml": "number — optional: grams per ml (e.g. olive oil ≈ 0.92, honey ≈ 1.42); defaults to 1.0 if not set",
  "nutrition_per_100g": {
    "calories": "number (kcal)",
    "macronutrients": {
      "protein":             "number (g)",
      "carbohydrates":       "number (g)",
      "fat":                 "number (g)",
      "fiber":               "number (g)",
      "sugar":               "number (g)",
      "saturated_fat":       "number (g)",
      "trans_fat":           "number (g)",
      "polyunsaturated_fat": "number (g)",
      "monounsaturated_fat": "number (g)",
      "added_sugars":        "number (g)",
      "cholesterol":         "number (mg)"
    },
    "micronutrients": {
      "vitamins": {
        "vitamin_a":   "number (mcg RAE)",
        "vitamin_c":   "number (mg)",
        "vitamin_d":   "number (mcg)",
        "vitamin_e":   "number (mg)",
        "vitamin_k":   "number (mcg)",
        "thiamine":    "number (mg)",
        "riboflavin":  "number (mg)",
        "niacin":      "number (mg)",
        "vitamin_b6":  "number (mg)",
        "folate":      "number (mcg DFE)",
        "vitamin_b12": "number (mcg)"
      },
      "minerals": {
        "calcium":    "number (mg)",
        "iron":       "number (mg)",
        "magnesium":  "number (mg)",
        "phosphorus": "number (mg)",
        "potassium":  "number (mg)",
        "zinc":       "number (mg)",
        "copper":     "number (mg)",
        "manganese":  "number (mg)",
        "selenium":   "number (mcg)",
        "sodium":     "number (mg)"
      }
    }
  },
  "environmental_impact": {
    "carbon_g_co2e_per_kg": "number — optional",
    "water_l_per_kg":       "number — optional",
    "land_m2_per_kg":       "number — optional"
  },
  "metadata": {
    "source":       "usda | edamam | open_food_facts | manual",
    "source_id":    "string — original ID in source system",
    "last_updated": "ISO 8601 timestamp",
    "data_quality": "high | medium | low"
  }
}
```

**Required fields:** `id`, `name`, `category`, `nutrition_per_100g.calories`, `metadata.source`, `metadata.last_updated`

**Data quality tiers:**
- `high` — USDA Foundation Foods; complete macro + micro data
- `medium` — Secondary API; macros complete, some micros missing
- `low` — Manual entry or incomplete API data; macros only

**Validation rules:**
- `name` must be unique (case-insensitive) in the database
- All numeric nutrition values must be ≥ 0
- `calories` must be consistent with macros: `(protein × 4) + (carbohydrates × 4) + (fat × 9)` within ±5%

---

### 4.2 Recipe

Represents a dish composed of ingredients. Per-serving nutrition is always computed, never manually set.

```json
{
  "id": "uuid-v4",
  "name": "string",
  "description": "string — optional",
  "servings": "integer ≥ 1",
  "ingredients": [
    {
      "ingredient_id":   "uuid-v4 — references Ingredient.id",
      "ingredient_name": "string — denormalised for readability",
      "amount":          "number > 0",
      "unit":            "grams | ml | tsp | tbsp | cup | large_unit | medium_unit | small_unit"
    }
  ],
  "prep_instructions":  ["string — optional ordered steps"],
  "cook_instructions":  ["string — required, ≥ 1 step"],
  "prep_time_minutes":  "integer ≥ 0",
  "cook_time_minutes":  "integer ≥ 0",
  "tags":               ["string — e.g. vegan, high-protein, quick"],
  "image_id":           "uuid-v4 — optional, references a stored image binary in the database",
  "status":             "complete | incomplete — set by backend, never by client",
  "nutrition_total":    "< NutritionBlock — see §4.6 >",
  "nutrition_per_serving": "< NutritionBlock — see §4.6 >",
  "metadata": {
    "created_at":  "ISO 8601 timestamp",
    "updated_at":  "ISO 8601 timestamp",
    "source":      "manual | imported_url",
    "source_url":  "string — if imported, optional"
  }
}
```

**Required fields:** `id`, `name`, `servings`, `ingredients` (≥ 1), `cook_instructions` (≥ 1), `prep_time_minutes`, `cook_time_minutes`

**Status rule:** `status` is `complete` by default. It is set to `incomplete` by the backend when any `ingredient_id` in the ingredients list no longer exists in the database (triggered on ingredient delete). It is restored to `complete` when all broken references are resolved by the user.

**Image storage:** Images are uploaded by the user and stored as binary (bytea) in the database, linked to the recipe via `image_id`. The backend serves the image via `GET /recipes/{id}/image`. Accepted formats: JPEG, PNG, WebP. Max size: 5MB.

**Computation rule:** `nutrition_total` and `nutrition_per_serving` are computed by the backend and stored on every create or update of the recipe. They are never set by the client.

**Unit conversion constants** (all ingredient amounts are converted to grams for nutrition calculation):

| Unit | Grams |
|------|-------|
| `grams` | 1.0 |
| `ml` | `ingredient.density_g_per_ml` if defined, else `1.0` |
| `tsp` | 4.2 |
| `tbsp` | 12.6 |
| `cup` | 240.0 |
| `large_unit` | `ingredient.unit_weights.large_unit_g` — must be defined on the ingredient |
| `medium_unit` | `ingredient.unit_weights.medium_unit_g` — must be defined on the ingredient |
| `small_unit` | `ingredient.unit_weights.small_unit_g` — must be defined on the ingredient |

**Nutrition calculation rule:**
```
for each ingredient:
    grams = convert(amount, unit)
    contribution = ingredient.nutrition_per_100g × (grams / 100)
nutrition_total = sum(contributions)
nutrition_per_serving = nutrition_total / servings
```

---

### 4.3 Menu

Represents a meal plan spanning one or more days.

```json
{
  "id": "uuid-v4",
  "name": "string",
  "start_date": "YYYY-MM-DD",
  "end_date":   "YYYY-MM-DD",
  "days": [
    {
      "date": "YYYY-MM-DD",
      "meals": {
        "breakfast": ["recipe_id"],
        "lunch":     ["recipe_id"],
        "dinner":    ["recipe_id"],
        "snack":     ["recipe_id"]
      }
    }
  ],
  "metadata": {
    "created_at": "ISO 8601 timestamp",
    "updated_at": "ISO 8601 timestamp"
  }
}
```

**Rules:**
- `end_date` must be ≥ `start_date`
- Each meal slot is an array — multiple recipes per slot are supported (e.g. two snacks)
- A recipe may appear multiple times across the menu

**Nutrition computation:** Menu nutrition is **never stored**. It is computed on demand by the backend when the frontend requests analysis. The frontend passes the `menu_id`; the backend returns a `MenuNutritionAnalysis` object (see §4.7).

**"Active menu":** A frontend concept only — the menu currently open in the UI. The backend is stateless with respect to which menu is active; the frontend always passes `menu_id` explicitly in API calls.

---

### 4.4 User Settings

Stores user-configurable application settings, including analysis thresholds.

```json
{
  "analysis": {
    "deficiency_threshold_percent_dv": "integer — default 70",
    "excess_threshold_percent_dv":     "integer — default 150"
  }
}
```

**Rules:**
- `deficiency_threshold_percent_dv` must be between 1 and 100
- `excess_threshold_percent_dv` must be > 100
- Defaults are applied if no settings have been saved

---

### 4.5 Pantry Entry (Phase 4)

Tracks stock on hand for grocery deduction.

```json
{
  "ingredient_id": "uuid-v4",
  "ingredient_name": "string",
  "quantity_grams": "number ≥ 0",
  "updated_at": "ISO 8601 timestamp"
}
```

---

### 4.6 NutritionBlock (shared structure)

Reused across Recipe and Menu wherever nutrition totals appear.

```json
{
  "calories": "number (kcal)",
  "macronutrients": {
    "protein":             "number (g)",
    "carbohydrates":       "number (g)",
    "fat":                 "number (g)",
    "fiber":               "number (g)",
    "sugar":               "number (g)",
    "saturated_fat":       "number (g)",
    "trans_fat":           "number (g)",
    "polyunsaturated_fat": "number (g)",
    "monounsaturated_fat": "number (g)",
    "added_sugars":        "number (g)",
    "cholesterol":         "number (mg)"
  },
  "micronutrients": {
    "vitamins": {
      "vitamin_a":   "number (mcg RAE)",
      "vitamin_c":   "number (mg)",
      "vitamin_d":   "number (mcg)",
      "vitamin_e":   "number (mg)",
      "vitamin_k":   "number (mcg)",
      "thiamine":    "number (mg)",
      "riboflavin":  "number (mg)",
      "niacin":      "number (mg)",
      "vitamin_b6":  "number (mg)",
      "folate":      "number (mcg DFE)",
      "vitamin_b12": "number (mcg)"
    },
    "minerals": {
      "calcium":    "number (mg)",
      "iron":       "number (mg)",
      "magnesium":  "number (mg)",
      "phosphorus": "number (mg)",
      "potassium":  "number (mg)",
      "zinc":       "number (mg)",
      "copper":     "number (mg)",
      "manganese":  "number (mg)",
      "selenium":   "number (mcg)",
      "sodium":     "number (mg)"
    }
  }
}
```

---

### 4.7 MenuNutritionAnalysis (computed response)

Returned on demand by the backend. Never stored.

```json
{
  "menu_id": "uuid-v4",
  "days": [
    {
      "date": "YYYY-MM-DD",
      "nutrition_total": "< NutritionBlock — see §4.6 >"
    }
  ],
  "period_total":  "< NutritionBlock >",
  "daily_average": "< NutritionBlock >",
  "dri_comparison": [
    {
      "nutrient":            "string — e.g. protein, vitamin_c",
      "daily_average_value": "number",
      "dri_value":           "number",
      "unit":                "string",
      "percent_dv":          "number",
      "status":              "deficient | adequate | excess"
    }
  ]
}
```

---

### 4.8 DRI Reference Values

Analysis uses the **universal 2000 kcal adult baseline** as the default. These values represent 100% Daily Value.

> Personal targets override these defaults in Phase 2 (FR-3.5). See Appendix A for source and assumptions.

| Nutrient | Daily Value | Unit |
|---------|------------|------|
| Calories | 2000 | kcal |
| Protein | 50 | g |
| Carbohydrates | 275 | g |
| Fat | 78 | g |
| Fiber | 28 | g |
| Saturated Fat | 20 | g |
| Sodium | 2300 | mg |
| Potassium | 4700 | mg |
| Calcium | 1300 | mg |
| Iron | 18 | mg |
| Magnesium | 420 | mg |
| Phosphorus | 1250 | mg |
| Zinc | 11 | mg |
| Copper | 0.9 | mg |
| Manganese | 2.3 | mg |
| Selenium | 55 | mcg |
| Vitamin A | 900 | mcg RAE |
| Vitamin C | 90 | mg |
| Vitamin D | 20 | mcg |
| Vitamin E | 15 | mg |
| Vitamin K | 120 | mcg |
| Thiamine (B1) | 1.2 | mg |
| Riboflavin (B2) | 1.3 | mg |
| Niacin (B3) | 16 | mg NE |
| Vitamin B6 | 1.7 | mg |
| Folate | 400 | mcg DFE |
| Vitamin B12 | 2.4 | mcg |
| Cholesterol | 300 | mg |

> Source: FDA Daily Values (2020) for adults and children ≥ 4 years. See Appendix A for full reference and assumptions.

---

## 5. Feature Specification

### Phase 1 — MVP

**Goal:** Working web application covering the full core workflow: ingredient management → recipe builder → weekly menu planner → nutritional analysis → grocery list.

---

#### FR-1: Ingredient Management

| ID | Feature | Description |
|----|---------|-------------|
| FR-1.1 | Import from USDA | User triggers search by name; backend queries USDA, normalises result, persists; frontend confirms |
| FR-1.2 | Import from Open Food Facts | User triggers search by name or barcode; backend queries OFF, normalises, persists; frontend confirms |
| FR-1.3 | Manual create | User fills ingredient form in frontend; backend validates against schema and saves |
| FR-1.4 | View / browse | Frontend lists all ingredients; search by name or alias; filter by category; view full nutrition profile |
| FR-1.5 | Duplicate detection | On import or manual create, backend detects name/alias collision; frontend prompts to merge or skip |

**Import workflow (applies to FR-1.1 and FR-1.2):**
1. User searches by name (or barcode for Open Food Facts) in the frontend
2. Backend queries the relevant API and returns ranked results
3. Frontend displays results (name, category, data quality)
4. User selects one result
5. Backend maps API fields to Ingredient schema (see §7), validates, and saves
6. Frontend confirms success and shows the saved ingredient

---

#### FR-1 (continued)

| ID | Feature | Description |
|----|---------|-------------|
| FR-1.6 | Delete ingredient | Remove ingredient from database. Any recipe referencing it is flagged `incomplete` and locked until the user resolves it (replace or remove the broken ingredient link). |

**Incomplete recipe:** A recipe becomes `incomplete` when one or more of its ingredient references no longer exists in the database. Incomplete recipes cannot be added to menus. The frontend shows a warning and a repair flow (substitute ingredient or remove line).

---

#### FR-2: Recipe Builder

| ID | Feature | Description |
|----|---------|-------------|
| FR-2.1 | Create recipe | Name, servings, ingredients from database with amounts and units, cook instructions, optional image upload |
| FR-2.2 | Auto-calc nutrition | On every save or update: backend computes and stores `nutrition_total` and `nutrition_per_serving` per §4.2 calculation rule |
| FR-2.3 | View recipe | Display recipe with ingredient list, instructions, per-serving NutritionBlock, and image if present |
| FR-2.6 | Delete recipe | Remove recipe from database. Any menu slot referencing it is cleared. User is warned before deletion if the recipe is in use. |

---

#### FR-3: Menu Planner

| ID | Feature | Description |
|----|---------|-------------|
| FR-3.1 | Create menu | Name, start date, end date |
| FR-3.2 | Assign recipes | Assign recipes to any date + meal type slot within the menu range; only non-incomplete recipes can be assigned |
| FR-3.3 | Nutrition on demand | Frontend requests nutrition analysis for a menu by ID; backend computes and returns a `MenuNutritionAnalysis` object (§4.7); result is not stored |
| FR-3.4 | View menu | Full date range view with per-day meal assignments |
| FR-3.8 | Delete menu | Remove menu from database. No cascade effects on recipes. |

---

#### FR-4: Nutritional Analysis

| ID | Feature | Description |
|----|---------|-------------|
| FR-4.1 | DRI comparison | Backend compares menu's daily average NutritionBlock against §4.8 DRI; frontend displays as % DV |
| FR-4.2 | Deficiency flagging | Flag nutrients below the deficiency threshold (default 70% DV, user-configurable via FR-4.5) |
| FR-4.3 | Excess flagging | Flag nutrients above the excess threshold (default 150% DV, user-configurable via FR-4.5) |
| FR-4.4 | Summary report | Visual summary listing flagged nutrients with % DV, direction, and colour coding |
| FR-4.5 | Configurable thresholds | User can set custom deficiency and excess % DV thresholds via the settings UI; stored in User Settings (§4.4) |

---

#### FR-5: Grocery List

| ID | Feature | Description |
|----|---------|-------------|
| FR-5.1 | Generate list | Backend derives full ingredient list from all recipes in the active menu; aggregates quantities |
| FR-5.2 | View and edit | Frontend displays the list grouped by ingredient category; user can remove or adjust items |
| FR-5.3 | Export | Export shopping list as plain text or PDF |

---

### Phase 2 — Enhanced Usability

| ID | Feature |
|----|---------|
| FR-2.4 | Edit and duplicate recipes; recalculate nutrition on change |
| FR-2.5 | Import recipe from URL (scrape + parse + ingredient matching) |
| FR-3.5 | Nutrition goal setting: custom daily targets for calories, macros, micros |
| FR-3.6 | Goal tracking: compare active menu against personal targets |
| FR-3.7 | Menu templates: save and reapply successful menu structures |
| FR-4.6 | Multi-week pattern analysis: identify recurring deficiencies across multiple menus |
| FR-1.7 | Edamam integration as additional ingredient source |

---

### Phase 3 — Community + Advanced

| ID | Feature |
|----|---------|
| FR-6.1 | Recipe suggestions based on identified nutrient deficiencies |
| FR-6.2 | Environmental impact display (using optional `environmental_impact` fields from §4.1) |
| FR-6.3 | Multi-user support: accounts, shared recipe library |
| FR-6.4 | Community recipe sharing and discovery |

---

### Phase 4 — Grocery Agent

**Goal:** Close the loop from menu plan to supermarket order.

#### Pipeline

```
Active menu plan
      ↓
[ Extract ]   Derive full ingredient list from all recipes in the menu
      ↓
[ Aggregate ] Combine quantities of repeated ingredients across recipes
      ↓
[ Deduct ]    Subtract pantry stock (see §4.4)
      ↓
[ Compare ]   Price-check across supported retailers
      ↓
[ Recommend ] Suggest single vs multi-retailer split with cost breakdown
      ↓
[ Order ]     Generate basket links (Phase 4.1) → place orders (Phase 4.2)
```

#### Supported Retailers (Brussels)

| Retailer | Model | Key Advantage |
|---------|-------|--------------|
| Colruyt / Collect&Go | Click & collect (free) | Legally guaranteed lowest prices |
| Delhaize | Home delivery + collect | Subscription €10/mo unlimited delivery |
| Carrefour | Home delivery | Wide range, frequent promotions |
| Crisp | Home delivery | Premium fresh produce, strong UX |

**Supermarket data note:** None of the target Belgian retailers (Colruyt, Delhaize, Lidl, Aldi, Carrefour) provide official public APIs for product catalogs or prices. Options for Phase 4 data ingestion are: (a) Open Prices by Open Food Facts (`prices.openfoodfacts.org`) — crowd-sourced, has a REST API, covers Belgian stores to some extent; (b) web scraping individual retailer websites — fragile and subject to ToS; (c) manual product entry. A technical spike to evaluate option (a) is required before committing to an implementation approach.

The user's vision for this layer: aggregate ingredient weights from the menu → find real supermarket products that cover those quantities (e.g. "need 500g flour" → "Farine de blé 1kg €0.89 at Colruyt") → recommend an optimised basket split.

#### Phase 4.1 — Foundation

| ID | Feature |
|----|---------|
| FR-7.1 | Menu → ingredient extraction and quantity aggregation (reuses recipe/menu data) |
| FR-7.2 | Supermarket product catalog ingestion: ingest product names, sizes, and prices per retailer |
| FR-7.3 | Product matching: given a required quantity, find the smallest adequate package from the catalog |
| FR-7.4 | Price comparison across Colruyt and Delhaize; recommend basket split |
| FR-7.5 | Output: itemised basket per retailer with quantities, products, and estimated total |
| FR-7.6 | Basic weekly spend tracking |

#### Phase 4.2 — Automation

| ID | Feature |
|----|---------|
| FR-7.7 | Direct integration with Colruyt Collect&Go and Delhaize online APIs |
| FR-7.8 | Automated order placement with user confirmation step |
| FR-7.9 | Delivery slot selection |
| FR-7.10 | Out-of-stock handling: auto-suggest alternatives |

#### Phase 4.3 — Intelligence

| ID | Feature |
|----|---------|
| FR-7.11 | Real-time price monitoring + opportunistic buy alerts |
| FR-7.12 | Auto pantry deduction from delivery confirmations |
| FR-7.13 | Menu suggestion engine based on seasonal pricing |
| FR-7.14 | Full multi-retailer split optimisation |

---

## 6. Backend REST API

All endpoints are prefixed with `/api`. Request and response bodies use `camelCase` JSON. All write operations validate input before persisting. Error responses always include a `message` field.

### Standard error response
```json
{ "message": "string — human-readable description" }
```

### HTTP status codes used
| Code | Meaning |
|------|---------|
| `200` | Success |
| `201` | Resource created |
| `204` | Success, no body (deletes) |
| `400` | Invalid input or business rule violation |
| `404` | Resource not found |
| `409` | Conflict — e.g. duplicate ingredient name |
| `422` | Unprocessable — e.g. broken ingredient reference |
| `502` | External API error (ingest endpoints only) |

---

### 6.1 Ingredients

#### `GET /api/ingredients`
List all ingredients.

| Param | Type | Description |
|-------|------|-------------|
| `search` | query string | Filter by name or alias (case-insensitive, partial match) |
| `category` | query string | Filter by category enum value |
| `dataQuality` | query string | Filter by `high \| medium \| low` |

**Response 200:** Array of full Ingredient objects.

---

#### `GET /api/ingredients/{id}`
Get a single ingredient.

**Response 200:** Full Ingredient object.
**Response 404:** Not found.

---

#### `POST /api/ingredients`
Create an ingredient manually.

**Request body:** Ingredient fields excluding `id` and `metadata.lastUpdated`. `metadata.source` must be `manual`.

**Response 201:** Created Ingredient object.
**Response 400:** Schema validation failure.
**Response 409:** `{ "message": "...", "existingId": "uuid" }` — name collision with existing ingredient.

---

#### `PUT /api/ingredients/{id}`
Update an ingredient (any field). Triggers nutrition recalculation on all complete recipes that use it.

**Request body:** Partial Ingredient fields.

**Response 200:** Updated Ingredient object.
**Response 404:** Not found.
**Response 409:** Name conflicts with a different existing ingredient.

---

#### `DELETE /api/ingredients/{id}`
Delete an ingredient. All recipes referencing it are set to `status: incomplete`.

**Response 204:** Deleted.
**Response 404:** Not found.

---

#### `GET /api/ingest/usda/search?q={name}`
Search USDA FoodData Central by name. Returns candidates only — nothing is persisted.

**Response 200:**
```json
[
  {
    "fdcId": "string",
    "name": "string",
    "category": "string",
    "dataType": "Foundation | SR Legacy",
    "dataQuality": "high | medium"
  }
]
```
**Response 502:** USDA API unreachable or returned an error.

---

#### `POST /api/ingest/usda/import`
Fetch a USDA result by ID, map to Ingredient schema, validate, and save.

**Request body:**
```json
{
  "fdcId": "string",
  "overrides": { "name": "string — optional, user-edited name" }
}
```

**Response 201:** Created Ingredient object.
**Response 409:** Duplicate name — body includes `existingId`.
**Response 502:** USDA API error.

---

#### `GET /api/ingest/off/search?q={name}` or `?barcode={barcode}`
Search Open Food Facts. `q` and `barcode` are mutually exclusive. Returns candidates — nothing is persisted.

**Response 200:**
```json
[
  {
    "offId": "string",
    "name": "string",
    "category": "string",
    "dataQuality": "medium"
  }
]
```
**Response 400:** Both `q` and `barcode` provided, or neither.
**Response 502:** OFF API error.

---

#### `POST /api/ingest/off/import`
Fetch an Open Food Facts result by ID, map to Ingredient schema, validate, and save.

**Request body:**
```json
{
  "offId": "string",
  "overrides": { "name": "string — optional" }
}
```

**Response 201:** Created Ingredient object.
**Response 409:** Duplicate name — body includes `existingId`.
**Response 502:** OFF API error.

---

### 6.2 Recipes

#### `GET /api/recipes`
List all recipes.

| Param | Type | Description |
|-------|------|-------------|
| `status` | query string | Filter by `complete \| incomplete` |
| `search` | query string | Filter by name (partial match) |

**Response 200:** Array of Recipe objects including `status` and `nutritionPerServing`.

---

#### `GET /api/recipes/{id}`
Get a single recipe.

**Response 200:** Full Recipe object.
**Response 404:** Not found.

---

#### `POST /api/recipes`
Create a recipe. Backend computes and stores `nutritionTotal` and `nutritionPerServing` on creation.

**Request body:** Recipe fields excluding `id`, `status`, `nutritionTotal`, `nutritionPerServing`, `metadata`.

**Response 201:** Created Recipe object with computed nutrition and `status: complete`.
**Response 400:** Schema validation error.
**Response 422:** An `ingredientId` in the ingredients list does not exist in the database.

---

#### `PUT /api/recipes/{id}`
Update a recipe. Backend recomputes and stores nutrition if ingredients or servings changed.

**Request body:** Partial Recipe fields.

**Response 200:** Updated Recipe object.
**Response 404:** Not found.
**Response 422:** An `ingredientId` does not exist in the database.

---

#### `DELETE /api/recipes/{id}`
Delete a recipe. All menu slots referencing it are cleared.

**Response 204:** Deleted.
**Response 404:** Not found.

---

#### `GET /api/recipes/{id}/image`
Serve the recipe image.

**Response 200:** Image binary. `Content-Type: image/jpeg | image/png | image/webp`.
**Response 404:** Recipe or image not found.

---

#### `POST /api/recipes/{id}/image`
Upload or replace the recipe image.

**Request:** `multipart/form-data`, field name `file`. Accepted: JPEG, PNG, WebP. Max 5 MB.

**Response 200:** `{ "imageId": "uuid" }`
**Response 400:** Unsupported format or file exceeds 5 MB.
**Response 404:** Recipe not found.

---

### 6.3 Menus

#### `GET /api/menus`
List all menus.

**Response 200:** Array of Menu objects (assignments only, no nutrition).

---

#### `GET /api/menus/{id}`
Get a single menu.

**Response 200:** Full Menu object (assignments only).
**Response 404:** Not found.

---

#### `POST /api/menus`
Create a menu.

**Request body:**
```json
{ "name": "string", "startDate": "YYYY-MM-DD", "endDate": "YYYY-MM-DD" }
```

**Response 201:** Created Menu object.
**Response 400:** `endDate` is before `startDate`.

---

#### `PUT /api/menus/{id}`
Update a menu — name, dates, or meal slot assignments.

**Request body:** Partial Menu fields. To assign a recipe, include the updated `days` array.

**Response 200:** Updated Menu object.
**Response 400:** Recipe is `incomplete`; date is outside the menu range.
**Response 404:** Not found.

---

#### `DELETE /api/menus/{id}`
Delete a menu.

**Response 204:** Deleted.
**Response 404:** Not found.

---

#### `GET /api/menus/{id}/nutrition`
Compute the full nutrition analysis on demand. Not stored. Applies user settings thresholds (§4.4) when determining `status` in `driComparison`.

**Response 200:** `MenuNutritionAnalysis` object (§4.7).
**Response 404:** Menu not found.
**Response 422:** Menu has no recipes assigned.

---

#### `GET /api/menus/{id}/grocery-list`
Compute the aggregated grocery list on demand. Not stored. Quantities are in grams.

**Response 200:**
```json
{
  "menuId": "uuid",
  "items": [
    {
      "ingredientId": "uuid",
      "ingredientName": "string",
      "category": "string",
      "totalGrams": "number"
    }
  ]
}
```
**Response 404:** Menu not found.
**Response 422:** Menu has no recipes assigned.

---

### 6.4 Settings

#### `GET /api/settings`
Get current user settings. Returns defaults if never explicitly saved.

**Response 200:**
```json
{
  "analysis": {
    "deficiencyThresholdPercentDv": 70,
    "excessThresholdPercentDv": 150
  }
}
```

---

#### `PUT /api/settings`
Update user settings.

**Request body:** Partial or full settings object.

**Response 200:** Updated settings object.
**Response 400:** `deficiencyThresholdPercentDv` > 100, or `excessThresholdPercentDv` ≤ 100.

---

## 7. External API Integration Contracts

### 7.1 USDA FoodData Central

- **Base URL:** `https://api.nal.usda.gov/fdc/v1/`
- **Auth:** API key via query param `api_key`
- **Search:** `GET /foods/search?query=<name>&dataType=Foundation,SR Legacy&pageSize=10`
- **Detail:** `GET /food/<fdcId>`

**Field mapping (USDA → Ingredient schema):**

| USDA field | Ingredient field | Notes |
|-----------|----------------|-------|
| `description` | `name` | User may edit before saving |
| `foodCategory` | `category` | Map to schema category enum |
| `fdcId` | `metadata.source_id` | |
| `Nutrient: Energy` | `nutrition_per_100g.calories` | kcal |
| `Nutrient: Protein` | `nutrition_per_100g.macronutrients.protein` | g |
| `Nutrient: Total lipid (fat)` | `nutrition_per_100g.macronutrients.fat` | g |
| `Nutrient: Carbohydrate, by difference` | `nutrition_per_100g.macronutrients.carbohydrates` | g |
| `Nutrient: Fiber, total dietary` | `nutrition_per_100g.macronutrients.fiber` | g |
| `Nutrient: Sugars, total including NLEA` | `nutrition_per_100g.macronutrients.sugar` | g |
| `Nutrient: Fatty acids, total saturated` | `nutrition_per_100g.macronutrients.saturated_fat` | g |
| `Nutrient: Fatty acids, total trans` | `nutrition_per_100g.macronutrients.trans_fat` | g |
| `Nutrient: Cholesterol` | `nutrition_per_100g.macronutrients.cholesterol` | mg |
| `Nutrient: Sodium, Na` | `nutrition_per_100g.micronutrients.minerals.sodium` | mg |
| `Nutrient: Calcium, Ca` | `nutrition_per_100g.micronutrients.minerals.calcium` | mg |
| `Nutrient: Iron, Fe` | `nutrition_per_100g.micronutrients.minerals.iron` | mg |
| `Nutrient: Vitamin C, total ascorbic acid` | `nutrition_per_100g.micronutrients.vitamins.vitamin_c` | mg |
| `Nutrient: Vitamin A, RAE` | `nutrition_per_100g.micronutrients.vitamins.vitamin_a` | mcg RAE |
| `Nutrient: Vitamin D (D2 + D3)` | `nutrition_per_100g.micronutrients.vitamins.vitamin_d` | mcg |
| *(remaining micros)* | *(corresponding field)* | Match by nutrient name |

**Data quality assignment:** Foundation Foods → `high`; SR Legacy → `medium`

**Error handling:** On API failure, surface error to user. Never partially save an ingredient.

### 7.2 Open Food Facts

- **Base URL:** `https://world.openfoodfacts.org/api/v2/`
- **Auth:** None required for read access
- **Search by name:** `GET /search?search_terms=<name>&fields=product_name,nutriments,categories&page_size=10`
- **Search by barcode:** `GET /product/<barcode>.json`

**Field mapping (Open Food Facts → Ingredient schema):**

| OFF field | Ingredient field | Notes |
|-----------|----------------|-------|
| `product_name` | `name` | User may edit before saving |
| `categories_tags` | `category` | Map to schema category enum |
| `_id` | `metadata.source_id` | Barcode |
| `nutriments.energy-kcal_100g` | `nutrition_per_100g.calories` | kcal |
| `nutriments.proteins_100g` | `nutrition_per_100g.macronutrients.protein` | g |
| `nutriments.fat_100g` | `nutrition_per_100g.macronutrients.fat` | g |
| `nutriments.carbohydrates_100g` | `nutrition_per_100g.macronutrients.carbohydrates` | g |
| `nutriments.fiber_100g` | `nutrition_per_100g.macronutrients.fiber` | g |
| `nutriments.sugars_100g` | `nutrition_per_100g.macronutrients.sugar` | g |
| `nutriments.saturated-fat_100g` | `nutrition_per_100g.macronutrients.saturated_fat` | g |
| `nutriments.sodium_100g` | `nutrition_per_100g.micronutrients.minerals.sodium` | mg (×1000) |
| *(remaining micros where available)* | *(corresponding field)* | OFF micro coverage is variable |

**Data quality assignment:** OFF data is typically `medium` (macros usually present; micros often missing).

**Error handling:** On API failure, surface error to user. Never partially save an ingredient.

---

## 8. Non-Functional Requirements

### 8.1 Performance

| Requirement | Target |
|------------|--------|
| External API requests | Complete within 3s; timeout at 5s with retry |
| Local data queries | Complete within 500ms |
| Menu nutrition calculation | Complete within 2s |
| Ingredient database size | Support 1000+ items without degradation |

### 8.2 Reliability

- No data loss: validate all writes before committing; rollback on failure
- API unavailability: surface a clear error to the user; never silently skip data
- All writes validated against schema before persistence

### 8.3 Portability

- Platform-agnostic: works on Windows, macOS, Linux
- No vendor lock-in for storage
- API keys stored in environment variables or local config file — never in version control

---

## 9. Conventions & Standards

### Naming
- Backend code identifiers: `snake_case` (Python)
- Internal data model field names: `snake_case`
- REST API request and response JSON fields: `camelCase` (JavaScript convention for frontend consumption)
- IDs: UUID v4

### Stored Units (always)

| Dimension | Unit |
|-----------|------|
| Weight | grams |
| Volume | ml |
| Energy | kcal |
| Vitamins/minerals | as specified in §4.1 and §4.8 |

### Enums (exhaustive)

**Ingredient category:**
`protein | vegetable | grain_and_cereal | fruit | dairy | fat_and_oil | condiment_and_sauce | herb_and_spice | beverage | snack`

**Season:**
`all_year | winter | spring | summer | autumn`

**Recipe amount unit:**
`grams | ml | tsp | tbsp | cup | large_unit | medium_unit | small_unit`

**Meal type:**
`breakfast | lunch | dinner | snack`

**Data source:**
`usda | edamam | open_food_facts | manual`

**Data quality:**
`high | medium | low`

**Recipe source:**
`manual | imported_url`

**Recipe status:**
`complete | incomplete`

---

## 10. Frontend Specification

### 10.1 Tech Stack

| Concern | Technology |
|---------|-----------|
| Framework | React 18 (functional components + hooks) |
| Build tool | Vite |
| Styling | Tailwind CSS v3 |
| Component library | shadcn/ui |
| State management | React Query (server state) + React `useState`/`useContext` (UI state) |
| Drag and drop | `@dnd-kit/core` + `@dnd-kit/sortable` |
| Routing | React Router v6 |
| HTTP client | `fetch` (native) wrapped in React Query query/mutation hooks |
| Charts | Recharts |

### 10.2 Design System

#### Color Tokens

The color palette is derived from the existing NiceGUI scaffold (`src/app/main.py`) and must be applied consistently.

| Token | Hex | Usage |
|-------|-----|-------|
| `color-main` | `#E9E0D8` | App background, tab panels |
| `color-accent` | `#C49450` | Primary action buttons, active nav indicator |
| `color-green` | `#79A486` | Adequate nutrient bars, success badges |
| `color-dark` | `#161f27` | Header background, primary text |
| `color-light` | `#F7F8F8` | Card surfaces, input backgrounds |

Additional semantic tokens derived from the base palette:

| Token | Value | Usage |
|-------|-------|-------|
| `color-deficient` | `#C0614E` (red) | Below deficiency threshold bar segments |
| `color-excess` | `#C49450` (accent) | Above excess threshold bar segments |
| `color-border` | `#D6CCC4` | Card/input borders (tinted main) |

#### Typography

- Font family: `Inter` (Google Fonts), fallback `sans-serif`
- Headings: `font-bold`, `text-dark`
- Body: `text-sm` to `text-base`, `text-dark`
- Secondary/meta text: `text-xs`, `text-dark/60`

#### Component Defaults (shadcn/ui overrides via `tailwind.config.js`)

- Border radius: `rounded-xl` for cards; `rounded-lg` for buttons and inputs
- Card shadow: `shadow-sm`
- Button primary: `bg-accent text-light hover:bg-accent/90`
- Button destructive: `bg-red-500 text-white hover:bg-red-600`

---

### 10.3 App Shell

```
┌────────────────────────────────────────────────────────────────────────┐
│  [Noorish logo]   Menu   Recipes   Ingredients   Analysis   Grocery   ⚙ │  ← TopNav
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                        <view content>                                  │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**TopNav component rules:**
- Fixed at top; full width; background `color-dark`; text `color-light`
- Logo: "Noorish" in `font-extrabold text-2xl text-light`
- Nav links: `Menu | Recipes | Ingredients | Analysis | Grocery`
- Active link: underline or bottom-border indicator in `color-accent`
- Settings icon (⚙) on the far right; navigates to `/settings`
- No secondary navigation; no sidebar

---

### 10.4 Route Structure

| Route | View | Notes |
|-------|------|-------|
| `/` | Menu Planner | Landing view; redirects to most-recently opened menu or "create menu" prompt |
| `/menus/:id` | Menu Planner | Specific menu |
| `/recipes` | Recipe Library | |
| `/recipes/new` | Create Recipe | |
| `/recipes/:id` | Recipe Detail | Read-only with Edit button |
| `/recipes/:id/edit` | Edit Recipe | |
| `/ingredients` | Ingredient Database | |
| `/analysis/:menuId` | Nutrition Analysis | Requires a menu context |
| `/grocery/:menuId` | Grocery List | Requires a menu context |
| `/settings` | Settings | |

---

### 10.5 View Specifications

#### 10.5.1 Menu Planner (`/menus/:id`)

This is the **landing view** and the primary workspace of the application.

**Layout:**
```
┌──────────────────────────────────────────────────────────────────────┐
│  [< Prev week]   Mon 12 May · Tue 13 · Wed 14 · ... · Sun 18   [Next >] │
├────────────┬─────────────────────────────────────────────────────────┤
│            │  Mon   Tue   Wed   Thu   Fri   Sat   Sun                │
│ Breakfast  │  [+]   [card] [+]  ...                                  │
│ Lunch      │  ...                                                     │
│ Dinner     │  ...                                                     │
│ Snack      │  ...                                                     │
└────────────┴─────────────────────────────────────────────────────────┘
```

**Behaviour:**
- Week view by default; each row is a meal type, each column is a day
- Each cell that has no recipe shows a `[+]` add button; hovering also accepts a drop target
- Each assigned recipe renders as a compact **Recipe Card** (title + thumbnail if available + calorie count)
- Drag source: Recipe Card in the Recipe Sidebar (see below) or an already-assigned card in the grid
- Drop target: Any empty cell — dropping moves/assigns the recipe to that slot
- Dropping onto an occupied cell: appends the recipe to that slot (multiple recipes per slot are allowed; display as stacked cards)
- Removing a recipe from a slot: click × on the card in the cell
- Clicking a recipe card in the grid opens Recipe Detail (read-only) in a side sheet

**Recipe Sidebar:**
- Collapsible panel on the right (default: open)
- Search input at top
- Scrollable list of Recipe Cards (complete recipes only — `status: complete`)
- Cards are drag-enabled; dragging from here creates an assignment

**Menu selector:**
- Dropdown in the subheader area to switch between saved menus or create a new one
- "New menu" option opens a modal with: name (text), start date, end date

**Action buttons:**
- "View Nutrition" → navigates to `/analysis/:menuId`
- "Grocery List" → navigates to `/grocery/:menuId`

---

#### 10.5.2 Recipe Library (`/recipes`)

**Layout:**
- Search input (full-width at top) with filter chips: `Seasonal | Quick | Vegetarian | Incomplete`
- Responsive grid of Recipe Cards (3 columns on desktop, 2 on tablet)
- Each Recipe Card shows: thumbnail (placeholder if none), recipe name, cuisine type, prep + cook time, calorie count per serving, `incomplete` badge if `status: incomplete`
- FAB (floating action button) or header button: "+ New Recipe"

**Incomplete recipe handling:**
- Cards with `status: incomplete` display a red warning badge "Missing ingredients"
- Clicking opens Recipe Detail which surfaces the broken ingredient links with a "Fix" prompt

---

#### 10.5.3 Recipe Detail (`/recipes/:id`)

**Layout:**
- Full-width header: recipe image (or placeholder gradient), recipe name overlay, action buttons (Edit, Delete)
- Two-column layout below: left = details; right = nutrition summary

**Left column:**
- Metadata: cuisine type, prep time, cook time, servings, source URL (if any), season badge
- Ingredient table: ingredient name | amount | unit | grams equivalent
- Instructions (if available — plain text or ordered list)

**Right column:**
- Compact **NutritionBlock** summary (calories per serving, macro bars: protein / fat / carbs)
- Link: "Full nutritional analysis →" (requires assigning to a menu)

**Incomplete state:**
- Banner at top: "This recipe is missing ingredients and cannot be used in menus until fixed"
- Broken ingredient rows highlighted in red with an "Replace" button per row

---

#### 10.5.4 Create / Edit Recipe (`/recipes/new`, `/recipes/:id/edit`)

**Form sections:**

1. **Basic Info** — name (required), cuisine type, season, servings (required), prep time, cook time
2. **Image** — file upload (JPEG/PNG/WebP, max 5MB); preview thumbnail; remove button
3. **Ingredients** — live search input against the Ingredient Database (`GET /api/ingredients?search=`); selecting an ingredient adds a row with amount (number) and unit (dropdown from unit enum); rows are reorderable; remove button per row; ingredient count badge
4. **Instructions** — textarea; optional

**Nutrition preview:**
- Live-computed sidebar or bottom panel: as user adds/changes ingredient amounts, call `POST /api/recipes/preview` (or compute client-side using stored per-100g values) and display calorie + macro totals

**Save behaviour:**
- "Save" calls `POST /api/recipes` or `PUT /api/recipes/:id`
- On success: navigate to Recipe Detail
- Validation: name required; at least one ingredient required; servings > 0

---

#### 10.5.5 Ingredient Database (`/ingredients`)

**Layout:**
- Search input + category filter dropdown at top
- Table view: name | category | calories/100g | protein | fat | carbs | source | quality badge | actions
- Quality badge: `high` (green), `medium` (amber), `low` (grey)
- Actions per row: Edit (inline or modal), Delete (with confirm dialog)
- "Add Ingredient" button: opens a modal with two tabs — Search (USDA / OFF) and Manual

**Search tab (within Add Ingredient modal):**
- Source selector: `USDA FoodData Central | Open Food Facts`
- Search input → results list → preview of nutrition values → "Import" button
- Imported record is pre-filled in a review form; user may edit name and category before saving

**Manual tab:**
- Full ingredient form with all nutrition fields; required: name, category, calories/100g, protein, fat, carbs

---

#### 10.5.6 Nutrition Analysis (`/analysis/:menuId`)

**Layout:**
- Menu name + date range at top; "Menu: [selector]" to switch menu
- Two sections: **Nutrient Overview** (full week) and **Day-by-Day** (per date)

**Nutrient Overview:**
- One horizontal bar chart per nutrient (using Recharts `BarChart` in horizontal orientation)
- Bar represents `% DV achieved` for the week average
- Color coding:
  - `< deficiency_threshold_percent_dv` → `color-deficient` (red)
  - `deficiency_threshold_percent_dv` to `excess_threshold_percent_dv` → `color-green`
  - `> excess_threshold_percent_dv` → `color-excess` (amber)
- Reference line at 100% DV
- Reference lines at deficiency threshold and excess threshold (dashed, labelled)
- Tooltip on hover: nutrient name, absolute value, unit, % DV

**Day-by-Day section:**
- Row of day cards; each shows calorie total vs target with a small indicator
- Clicking a day card expands an inline nutrient breakdown for that day (same horizontal bar chart format)

**Data source:** Calls `GET /api/menus/:menuId/nutrition` on mount; loading skeleton while fetching.

---

#### 10.5.7 Grocery List (`/grocery/:menuId`)

**Layout:**
- Menu name at top; "Generate" button (or auto-generated on route entry)
- Table: ingredient name | category | total grams | (Phase 4: product match | price | store)
- Grouped by category (collapsible groups)
- "Export" button: download as plain-text or CSV

**Data source:** Calls `GET /api/menus/:menuId/grocery-list` on mount.

**Phase 4 additions (not implemented in Phase 1):**
- Each row will add: matched product name, unit count, estimated price, store selector
- "Order" or "Add to basket" links per item

---

#### 10.5.8 Settings (`/settings`)

**Sections:**

1. **Nutrition Thresholds**
   - Deficiency threshold: number input (% DV), default 70
   - Excess threshold: number input (% DV), default 150
   - Validation: deficiency < 100, excess > 100, deficiency < excess
   - "Save" button calls `PUT /api/settings`

2. **Data Sources** (Phase 2)
   - Toggle USDA / Open Food Facts (placeholder in Phase 1)

---

### 10.6 UX Patterns

#### Drag and Drop (Menu Planner)

- Library: `@dnd-kit/core`
- Drag handle: entire Recipe Card surface is draggable
- Visual feedback during drag: card becomes semi-transparent at source; drop targets highlight with a dashed border in `color-accent`
- On drop: optimistic UI update (place card immediately); fire `PUT /api/menus/:id` in background; revert on error with a toast
- Keyboard accessible: `@dnd-kit` handles keyboard drag natively

#### Loading States

- Skeleton loaders for all data-dependent content (cards, tables, charts)
- Use shadcn/ui `Skeleton` component
- Skeletons match the approximate shape of the content they replace (card skeleton, table row skeleton, bar chart skeleton)

#### Toast Notifications

- shadcn/ui `Sonner` toast
- Position: bottom-right
- Success: "Recipe saved", "Menu updated", etc. — auto-dismiss 3s
- Error: "Failed to save — please try again" — manual dismiss

#### Empty States

Each view with no data shows a centred illustration + message + primary action:

| View | Empty message | Action |
|------|--------------|--------|
| Recipe Library | "No recipes yet" | "+ Create your first recipe" |
| Menu Planner | "No menu selected" | "Create a menu" |
| Ingredient Database | "No ingredients found" | "Add an ingredient" |
| Nutrition Analysis | "Assign recipes to your menu to see analysis" | "Go to Menu Planner" |
| Grocery List | "No ingredients to list" | "Go to Menu Planner" |

#### Confirm Dialogs

Used before destructive actions (Delete Recipe, Delete Ingredient, Remove from Menu):
- shadcn/ui `AlertDialog`
- Message: "Delete [item name]? This cannot be undone."
- Buttons: "Cancel" (outline) | "Delete" (destructive red)
- Deleting an ingredient that is used in recipes: warning added — "X recipes will be marked incomplete"

#### Responsive Behaviour

- Desktop-first; target minimum viewport: 1024px wide
- Recipe grid: 3 cols → 2 cols at `lg` breakpoint → 1 col at `md`
- Menu Planner grid: scrollable horizontally on viewports narrower than 1024px
- Navigation: full horizontal top bar on all screen sizes; no hamburger menu required (Phase 1)

---

## Appendix A — Reference Values and Assumptions

### A.1 DRI Source

Daily Values in §4.8 are taken from:
> **FDA Daily Values (2020)** — "Daily Value on the Nutrition and Supplement Facts Labels", U.S. Food & Drug Administration.
> Applicable to adults and children aged 4 years and older; based on a 2000 kcal/day diet.
> Reference: https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels

### A.2 Assumptions and Deviations

| Nutrient | Assumption |
|---------|-----------|
| Cholesterol | FDA DV is 300mg (upper limit; no minimum DRI). Used as excess threshold only. |
| Niacin | Value is 16 mg Niacin Equivalents (NE); USDA reports as mg NE. |
| Folate | Value is 400 mcg Dietary Folate Equivalents (DFE); food sources only (not supplemental folic acid). |
| Vitamin A | Value is 900 mcg Retinol Activity Equivalents (RAE); USDA reports as mcg RAE. |
| Vitamin D | Value is 20 mcg (= 800 IU); some sources use 15 mcg (600 IU) for adults under 70. |

### A.3 Unit Weight Reference Values

Default `unit_weights` for common ingredients (used when importing from APIs that don't provide serving size data):

| Ingredient | small_unit_g | medium_unit_g | large_unit_g |
|-----------|------------|--------------|-------------|
| Egg | 38 | 44 | 50 |
| Apple | 100 | 150 | 200 |
| Tomato | 90 | 120 | 170 |
| Onion | 100 | 150 | 200 |
| Potato | 100 | 170 | 250 |
| Avocado | 150 | 200 | 250 |
| Lemon | 60 | 80 | 100 |
| Lime | 45 | 65 | 85 |
| Banana | 100 | 120 | 150 |
| Garlic clove | 3 | 5 | 7 |

> These are approximate averages. Individual ingredients in the database should have their `unit_weights` verified and corrected on import.
