# Imports
import os
from os.path import join
from utils import dump_json, create_folder_if_not_exists
from get_cards_data import get_cards_data
from dotenv import load_dotenv
load_dotenv()

# Parameters
LANGUAGES = ["fr"]
OUTPUT_FOLDER = "results"
MY_TOKEN = os.getenv("TOKEN")

if __name__ == "__main__":
    cards, types, subtypes, factions, rarities = get_cards_data(collection_token=MY_TOKEN)
    create_folder_if_not_exists(OUTPUT_FOLDER)
    dump_json(cards,    join(OUTPUT_FOLDER, 'collection.json'))