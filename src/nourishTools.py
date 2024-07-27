"""
    Nourish SW Tools

"""

# Importing
import json


###################
## Functions
###################

def load_json(file_path):
    """ Load data from JSON file """
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