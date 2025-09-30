from app.models.recipe import Recipe
from app.db import db

def create_recipe(data):
    recipe = Recipe(
        name = data["name"],
        ingredients = data["ingredients"],
        instructions = data.get("instructions"),
        tags = data.get("tags")
    )
    db.session.add(recipe)
    db.session.commit()
    return recipe

def get_all_recipes():
    """fetch all recipes from database"""
    return Recipe.query.all()