"""
Parse all receipts and update databases

"""

# Importing
import json
from os import listdir
from os.path import join
import pandas as pd

# Parameters
recipes_path = r"data\recipes"

# Secondary functions
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {file_path}")
        return None

# Parse recipes to collect product list
recipe_list = [f for f in listdir(recipes_path) if "template" not in f]
for recipe in recipe_list:
    # Get content
    content = load_json(join(recipes_path, recipe))
    
    # Get ingredients
    for ingredient in content["ingredients"]:
        ingredient_df = pd.DataFrame(ingredient)
        print("32")



# Update Pantry 

# Fetch nutrients from nutrition APIs

# Update Nutrients Database