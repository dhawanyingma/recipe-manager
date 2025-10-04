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

def get_recipe_by_id(recipe_id: int):
    """Fetch a singe recipe by ID or return None if not found."""
    return Recipe.query.get(recipe_id)

def update_recipe(recipe_id: int, data: dict):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return None
    if "name" in data:
        recipe.name = data["name"]
    if "ingredients" in data:
        recipe.ingredients = data["ingredients"]
    if "instructions" in data:
        recipe.instructions = data["instructions"]
    if "tags" in data:
        recipe.tags = data["tags"]
    db.session.commit()
    return recipe

def delete_recipe_service(recipe_id: int):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return False
    db.session.delete(recipe)
    db.session.commit()
    return True

def validate_recipe_data(data: dict):
    errors = {}
    if "name" not in data or not isinstance(data["name"], str) or len(data.get("name").strip()) <= 3:
        errors["name"] = "Name is required and must be at least 3 characters long."

    for field in ["ingredients", "instructions", "tags"]:
        if field in data and (not isinstance(data[field], str) or not data[field].strip()):
            errors[field] = f"{field} must be non-empty string if provided."

    return errors
        

