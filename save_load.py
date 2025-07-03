# Imports
import json
import os

DATA_FILE = "user_data.json"

# Load user inventory from JSON file
def load_user_inventory(username):
    if not os.path.exists(DATA_FILE): # If data file doesn't exist, return empty inventory
        return []

    with open(DATA_FILE, "r") as f: # Open existing data file
        data = json.load(f)
    return data.get(username, {}).get("inventory", []) # Return inventory for given username, or empty list if not found

# Save user inventory to JSON file
def save_user_inventory(username, inventory_items):
    if not os.path.exists(DATA_FILE): # If  data file doesn't exist, create empty one
        data = {}
    else:
        with open(DATA_FILE, "r") as f: # Open  existing data file
            data = json.load(f)

    if username not in data: # If username not in data, create new entry
        data[username] = {}

    data[username]["inventory"] = inventory_items

    with open(DATA_FILE, "w") as f: # Write updated data back to file
        json.dump(data, f, indent=2)