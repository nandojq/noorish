Fetch the recipe from this URL and add it to the Noorish database.

URL: $ARGUMENTS

## Steps

### 1. Fetch the page

Use WebFetch to retrieve the full content of the URL above.

### 2. Parse the recipe

Extract the recipe from the page content. Try in this order:
- **JSON-LD** (`<script type="application/ld+json">` containing `"@type": "Recipe"`)
- **Microdata / microformat** recipe markup
- **Plain HTML** — infer name, ingredients, instructions from the visible text

If you cannot find a recipe (no name, no ingredients, no instructions), stop and report:
> No recipe found at this URL. The page could not be parsed as a recipe.

### 3. Build the import payload

Map the parsed data to this JSON structure. All keys are **camelCase**:

```json
{
  "name": "<recipe title>",
  "description": "<short description or null>",
  "servings": <integer, default 4 if not stated>,
  "ingredients": [
    { "ingredientName": "<name>", "amount": <number>, "unit": "<unit>" }
  ],
  "prepInstructions": ["<step>", ...],
  "cookInstructions": ["<step>", ...],
  "prepTimeMinutes": <integer, 0 if unknown>,
  "cookTimeMinutes": <integer, 0 if unknown>,
  "tags": ["<tag>", ...],
  "source": "<website domain, e.g. ottolenghi.co.uk>",
  "sourceUrl": "<the original URL>"
}
```

**Unit normalisation** — only these values are accepted; convert everything else:

| Raw unit | Use |
|---|---|
| g / gram / grams | `grams` |
| tsp / teaspoon | `tsp` |
| tbsp / tablespoon | `tbsp` |
| cup | `cup` |
| ml / millilitre / milliliter | `ml` |
| l / litre / liter | `ml` (× 1000) |
| oz / ounce | `grams` (× 28.35) |
| lb / pound | `grams` (× 453.59) |
| kg / kilogram | `grams` (× 1000) |
| whole large item (e.g. large onion, large pepper) | `large_unit` |
| whole medium item (e.g. onion, carrot, clove) | `medium_unit` |
| whole small item (e.g. small shallot, cherry tomato) | `small_unit` |
| pinch | `tsp` with amount 0.1 |

Rules:
- `cookInstructions` must have at least one step. If the page only lists combined instructions put them all there.
- `servings` must be ≥ 1.
- Ingredient `amount` must be a positive number.
- Strip fractions (½ → 0.5, ¾ → 0.75, ⅓ → 0.33, ¼ → 0.25, etc.).

### 4. POST to the API

Use Bash to send the payload to the local Noorish backend:

```bash
python - <<'PYEOF'
import json, urllib.request, sys

payload = <PASTE_PAYLOAD_HERE>

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/recipes/import',
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
)
try:
    with urllib.request.urlopen(req) as r:
        body = json.loads(r.read().decode())
        print(f"SUCCESS — recipe added: {body['name']} (id: {body['id']})")
except urllib.error.HTTPError as e:
    print(f"ERROR {e.code}: {e.read().decode()}", file=sys.stderr)
    sys.exit(1)
PYEOF
```

### 5. Report the result

On success:
> Recipe added: **{name}** ({servings} servings) — id `{id}`

On API error, show the error body and suggest what might be wrong (e.g., missing instructions, bad unit).

On parse failure (no recipe detected), say so clearly without calling the API.
