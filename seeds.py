import os
import json

from app import create_app
from app.db import db
from app.models import Recipe

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SEED_FILE = os.path.join(BASE_DIR, "app/seeds", "recipes.json")

def load_seeds():
    with open(SEED_FILE, "r") as f:
        data = json.load(f)

    # insertables = []
    recipes = [
        Recipe(
        name = entry["name"],
        ingredients = entry["ingredients"],
        instructions = entry["instructions"],
        tags = entry["tags"]
        )
        for entry in data
        ]
    db.session.add_all(recipes)

    # db.session.add(insertables)
    db.session.commit()
    print(f"Inserted {len(data)} recipes into database")

if __name__ == "__main__":
    app = create_app("config.DevConfig")
    with app.app_context():
        load_seeds()