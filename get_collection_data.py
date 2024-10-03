# Imports
import os
from os.path import join
from utils import dump_json, create_folder_if_not_exists
from get_cards_data import get_cards_data

# Parameters
LANGUAGES = ["fr"]
OUTPUT_FOLDER = "data"

with open("token.txt", "r") as f:
    saved_token = f.read()

if __name__ == "__main__":
    collection, types, subtypes, factions, rarities = get_cards_data(collection_token=saved_token)
    create_folder_if_not_exists(OUTPUT_FOLDER)
    dump_json(collection,    join(OUTPUT_FOLDER, 'collection.json'))