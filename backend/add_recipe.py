import json
import urllib.request

url = 'http://127.0.0.1:8000/api/recipes/import'
payload = {
    'name': 'Festive hummus with roasted brussels sprouts and chestnuts',
    'description': 'Imported from Ottolenghi URL',
    'servings': 8,
    'ingredients': [
        {'ingredientName': 'Olive oil', 'amount': 120, 'unit': 'ml'},
        {'ingredientName': 'Sage leaves', 'amount': 10, 'unit': 'grams'},
        {'ingredientName': 'Cooked chestnuts', 'amount': 200, 'unit': 'grams'},
        {'ingredientName': 'Brussels sprouts', 'amount': 400, 'unit': 'grams'},
        {'ingredientName': 'Lemon', 'amount': 120, 'unit': 'grams'},
        {'ingredientName': 'Cooked chickpeas', 'amount': 500, 'unit': 'grams'},
        {'ingredientName': 'Garlic cloves', 'amount': 10, 'unit': 'grams'},
        {'ingredientName': 'Ground cumin', 'amount': 0.25, 'unit': 'tsp'},
        {'ingredientName': 'Tahini', 'amount': 120, 'unit': 'ml'},
        {'ingredientName': 'White balsamic vinegar', 'amount': 1, 'unit': 'tbsp'},
    ],
    'prepInstructions': [
        'Preheat the oven to 230C.',
        'Heat oil in a large tray and crisp the sage leaves.',
    ],
    'cookInstructions': [
        'Roast the chestnuts, brussels sprouts, lemon zest, salt and pepper until charred.',
        'Blend chickpeas, garlic, water, cumin, tahini and lemon juice until smooth.',
        'Whisk olive oil, lemon juice and white balsamic into a dressing.',
        'Assemble hummus, top with roasted vegetables, sage and the dressing.',
    ],
    'prepTimeMinutes': 15,
    'cookTimeMinutes': 20,
    'source': 'ottolenghi',
    'sourceUrl': 'https://ottolenghi.co.uk/pages/recipes/festive-hummus-roasted-brussels-sprouts-chestnuts',
}
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
)
with urllib.request.urlopen(req) as resp:
    print(resp.status)
    print(resp.read().decode('utf-8'))
