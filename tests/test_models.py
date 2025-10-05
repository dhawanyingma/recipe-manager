from app.models.recipe import Recipe
from app.db import db
from datetime import datetime

# tests/test_recipes.py
def test_basic_math():
    assert 2 + 2 == 4

def test_recipe_model_creation(client):
    recipe = Recipe(name = "soup", ingredients = "noodles, water", instructions = "boil")
    assert recipe.name == "soup"
    assert recipe.ingredients == "noodles, water"
    assert recipe.instructions == "boil"
    assert recipe.tags is None

def test_recipe_repr_returns_name(client):
    recipe = Recipe(name="Pasta")
    assert repr(recipe) == "<Recipe Pasta>"
