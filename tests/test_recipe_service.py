import pytest
from app.models.recipe import Recipe
from app.services.recipe_service import (
    create_recipe,
    get_all_recipes,
    get_recipe_by_id,
    update_recipe,
    delete_recipe_service,
    validate_recipe_data,
)
from app import db


# ---------------------------- CREATE ----------------------------

def test_create_recipe_success(client):
    """Test creating a recipe inserts record into DB."""
    data = {
        "name": "Pancakes",
        "ingredients": "Flour, Eggs, Milk",
        "instructions": "Mix and cook on pan.",
        "tags": "breakfast"
    }

    recipe = create_recipe(data)
    assert recipe.id is not None
    assert recipe.name == data["name"]

    # Confirm record exists in DB
    found = Recipe.query.get(recipe.id)
    assert found is not None
    assert found.name == "Pancakes"


# ---------------------------- GET ALL ----------------------------

def test_get_all_recipes(client):
    """Test fetching all recipes returns correct list."""
    create_recipe({"name": "A", "ingredients": "x", "instructions": "y"})
    create_recipe({"name": "B", "ingredients": "x", "instructions": "y"})

    recipes = get_all_recipes()
    assert isinstance(recipes, list)
    assert len(recipes) == 2
    assert all(isinstance(r, Recipe) for r in recipes)


# ---------------------------- GET BY ID ----------------------------

def test_get_recipe_by_id_success(client):
    """Test getting recipe by ID returns correct object."""
    recipe = create_recipe({"name": "Soup", "ingredients": "Water", "instructions": "Boil"})
    found = get_recipe_by_id(recipe.id)

    assert found is not None
    assert found.name == recipe.name


def test_get_recipe_by_id_not_found(client):
    """Test non-existing ID returns None."""
    result = get_recipe_by_id(9999)
    assert result is None


# ---------------------------- UPDATE ----------------------------

def test_update_recipe_success(client):
    """Test updating a recipe changes fields correctly."""
    recipe = create_recipe({"name": "Salad", "ingredients": "Veggies", "instructions": "Mix"})

    updated_data = {"name": "Greek Salad", "ingredients": "Cucumber, Feta, Tomato"}
    updated = update_recipe(recipe.id, updated_data)

    assert updated is not None
    assert updated.name == "Greek Salad"
    assert updated.ingredients == "Cucumber, Feta, Tomato"


def test_update_recipe_not_found(client):
    """Test updating non-existent recipe returns None."""
    result = update_recipe(9999, {"name": "Does Not Exist"})
    assert result is None


# ---------------------------- DELETE ----------------------------

def test_delete_recipe_success(client):
    """Test deleting existing recipe removes it from DB."""
    recipe = create_recipe({"name": "ToDelete", "ingredients": "X", "instructions": "Y"})

    result = delete_recipe_service(recipe.id)
    assert result is True

    deleted = Recipe.query.get(recipe.id)
    assert deleted is None


def test_delete_recipe_not_found(client):
    """Test deleting non-existent recipe returns False."""
    result = delete_recipe_service(9999)
    assert result is False


# ---------------------------- VALIDATION ----------------------------

@pytest.mark.parametrize("data", [
    {},  # completely empty
    {"name": ""},  # blank
    {"name": "ab"},  # too short
])
def test_validate_recipe_data_invalid(client, data):
    """Test invalid recipe data returns validation errors."""
    errors = validate_recipe_data(data)
    assert "name" in errors
    assert "at least 3 characters" in errors["name"]


def test_validate_recipe_data_valid(client):
    """Test valid data passes validation with no errors."""
    data = {
        "name": "Lasagna",
        "ingredients": "Pasta, Meat",
        "instructions": "Bake for 30 min",
        "tags": "italian"
    }
    errors = validate_recipe_data(data)
    assert errors == {}
