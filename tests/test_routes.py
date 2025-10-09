import pytest
import base64
from app.models.recipe import Recipe
from app import db

def test_health_check(client):
    response = client.get("/api/v1/health")
    data = response.get_json()
    assert response.status_code == 200
    assert data["status"] == "ok"

def test_version_check(client):
    response = client.get("/api/v1/version")
    data = response.get_json()
    assert response.status_code == 200
    assert data["version"] == "v1"

def test_create_recipe_success(client):
    payload = {
        "name": "Chocolate Cake",
        "ingredients": "Flour, Cocoa, Sugar, Eggs, Milk",
        "instructions": "Mix all ingredients and bake at 350F for 30 minutes."
    }
    response = client.post("/api/v1/recipes", json = payload)
    data = response.get_json()

    assert response.status_code == 201
    assert "id" in data
    assert data["name"] == payload["name"]

def test_create_recipe_validation(client):
    payload = {
        "ingredients": "Flour, Cocoa, Sugar, Eggs, Milk",
        "instructions": "Mix all ingredients and bake at 350F for 30 minutes."
    }    

    response = client.post("/api/v1/recipes", json = payload)
    data = response.get_json()

    assert response.status_code == 400
    assert data["errors"] == "VALIDATION_ERROR"
    assert "details" in data


def seed_recipes():
    """Helper to seed DB with sample recipes and fixed IDs."""
    recipes = [
        Recipe(id=1, name="Chocolate Cake", ingredients="Cocoa, Sugar", instructions="Bake"),
        Recipe(id=2, name="Chicken Curry", ingredients="Chicken, Spices", instructions="Cook"),
        Recipe(id=3, name="Pasta Alfredo", ingredients="Pasta, Cream", instructions="Boil"),
        Recipe(id=4, name="Chicken Soup", ingredients="Chicken, Salt", instructions="Boil"),
        Recipe(id=5, name="Veggie Salad", ingredients="Lettuce, Tomato", instructions="Mix"),
    ]
    db.session.bulk_save_objects(recipes)
    db.session.commit()
    return recipes


def test_get_recipes_basic_success(client):
    """Test fetching all recipes returns expected structure."""
    seed_recipes()

    response = client.get("/api/v1/recipes")
    data = response.get_json()

    assert response.status_code == 200
    assert "items" in data
    assert isinstance(data["items"], list)
    assert "limit" in data
    assert data["limit"] == 10  # default
    assert "total" in data
    assert data["total"] == 5
    assert len(data["items"]) <= 10


def test_get_recipes_with_limit(client):
    """Test limit parameter restricts number of results."""
    seed_recipes()

    response = client.get("/api/v1/recipes?limit=3")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["items"]) == 3
    assert data["limit"] == 3
    assert "next_page_token" in data
    # next_page_token should exist since more than 3 recipes exist
    assert data["next_page_token"] is not None


def test_get_recipes_invalid_limit(client):
    """Test invalid limit values return 400 error."""
    for invalid_limit in [0, 200, -5]:
        response = client.get(f"/api/v1/recipes?limit={invalid_limit}")
        data = response.get_json()

        assert response.status_code == 400
        assert "error" in data
        assert data["error"]["code"] == "INVALID_LIMIT"


def test_get_recipes_invalid_token(client):
    """Test invalid next_page_token returns 400 error."""
    seed_recipes()

    response = client.get("/api/v1/recipes?next_page_token=bad-token###")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"]["code"] == "INVALID_TOKEN"


def test_get_recipes_pagination(client):
    """Test pagination using next_page_token returns next set of results."""
    recipes = seed_recipes()

    # Page 1
    response1 = client.get("/api/v1/recipes?limit=2")
    data1 = response1.get_json()

    assert response1.status_code == 200
    assert len(data1["items"]) == 2
    next_token = data1["next_page_token"]
    assert next_token is not None

    # Page 2
    response2 = client.get(f"/api/v1/recipes?limit=2&next_page_token={next_token}")
    data2 = response2.get_json()

    assert response2.status_code == 200
    assert len(data2["items"]) >= 1  # could be 1 or 2 depending on total count
    # Ensure next page IDs are greater than previous page’s last ID
    first_page_last_id = data1["items"][-1]["id"]
    second_page_first_id = data2["items"][0]["id"]
    assert second_page_first_id > first_page_last_id
    # total should not exist in page 2
    assert "total" not in data2


def test_get_recipes_search_filter(client):
    """Test searching for 'chicken' returns only matching recipes."""
    seed_recipes()

    response = client.get("/api/v1/recipes?search=chicken")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["items"]) > 0
    for recipe in data["items"]:
        assert "chicken" in recipe["name"].lower()


def test_get_recipes_empty_result(client):
    """Test when no recipes exist returns empty list."""
    response = client.get("/api/v1/recipes")
    data = response.get_json()

    assert response.status_code == 200
    assert data["items"] == []
    assert data["total"] == 0

def test_get_recipe_success(client):
    """Test getting a recipe by ID returns correct data."""
    recipes = seed_recipes()
    recipe = recipes[0]

    response = client.get(f"/api/v1/recipes/{recipe.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data["id"] == recipe.id
    assert data["name"] == recipe.name
    assert data["ingredients"] == recipe.ingredients
    assert data["instructions"] == recipe.instructions


def test_get_recipe_not_found(client):
    """Test requesting a recipe ID that doesn't exist returns 404."""
    response = client.get("/api/v1/recipes/9999")
    data = response.get_json()

    assert response.status_code == 404
    assert "error" in data
    assert data["error"]["code"] == "NOT FOUND"
    assert "Recipe not found" in data["error"]["message"]    

# --------------------------- UPDATE ROUTE TESTS ---------------------------

def test_update_recipe_success(client):
    """Test updating a recipe successfully."""
    recipes = seed_recipes()
    recipe = recipes[0]

    update_payload = {
        "name": "Updated Cake",
        "ingredients": "Flour, Cocoa, Eggs",
        "instructions": "Bake at 350F for 40 minutes"
    }

    response = client.put(f"/api/v1/recipes/{recipe.id}", json=update_payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == recipe.id
    assert data["name"] == update_payload["name"]
    assert data["ingredients"] == update_payload["ingredients"]
    assert data["instructions"] == update_payload["instructions"]

    # Verify database was actually updated
    updated_recipe = Recipe.query.get(recipe.id)
    assert updated_recipe.name == update_payload["name"]


def test_update_recipe_not_found(client):
    """Test updating a non-existing recipe returns 404."""
    update_payload = {
        "name": "Ghost Recipe",
        "ingredients": "None",
        "instructions": "Does not exist"
    }

    response = client.put("/api/v1/recipes/9999", json=update_payload)
    data = response.get_json()

    assert response.status_code == 404
    assert "error" in data
    assert data["error"]["code"] == "NOT_FOUND"
    assert "Recipe no found" in data["error"]["message"]


# --------------------------- DELETE ROUTE TESTS ---------------------------

def test_delete_recipe_success(client):
    """Test deleting a recipe successfully."""
    recipes = seed_recipes()
    recipe = recipes[0]

    response = client.delete(f"/api/v1/recipes/{recipe.id}")
    text = response.get_data(as_text=True)

    assert response.status_code == 200
    assert f"The recipe with ID {recipe.id}" in text

    # Verify it was deleted from DB
    deleted = Recipe.query.get(recipe.id)
    assert deleted is None


def test_delete_recipe_not_found(client):
    """Test deleting a non-existing recipe returns 404."""
    response = client.delete("/api/v1/recipes/9999")
    data = response.get_json()

    assert response.status_code == 404
    assert "error" in data
    assert data["error"]["code"] == "NOT_FOUND"
    assert "Recipe not found" in data["error"]["message"]
