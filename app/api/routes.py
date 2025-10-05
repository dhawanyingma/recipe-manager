from flask import Blueprint, jsonify, request
from app.services.recipe_service import (
    create_recipe,
    get_all_recipes,
    get_recipe_by_id,
    update_recipe,
    delete_recipe_service,
    validate_recipe_data,
)
import base64
from sqlalchemy import func
from app.models.recipe import Recipe

api = Blueprint("api", __name__)


@api.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@api.route("/version", methods=["GET"])
def version():
    return jsonify({"version": "v1"}), 200


@api.route("/recipes", methods=["POST"])
def create_recipe_route():
    data = request.get_json() or {}
    print(data)
    errors = validate_recipe_data(data)
    print(errors)
    if errors:
        return (
            jsonify(
                {
                    "errors": "VALIDATION_ERROR",
                    "message": "Invalid request data",
                    "details": errors,
                }
            ),
            400,
        )
    recipe = create_recipe(data)
    return jsonify({"id": recipe.id, "name": recipe.name}), 201


# @api.route("/recipes", methods = ["GET"])
# def get_recipes_route():
#     recipes = get_all_recipes()
#     return jsonify([recipe.to_dict() for recipe in recipes]), 200


@api.route("/recipes", methods=["GET"])
def get_recipes_route():
    """
    GET /recipes
    Supports cursor-based pagination using 'next_page_token'.
    Also allows text search on recipe name using '?search=' query param
    Example requests:
        /recipes?limit=5
        /recipes?limit=5&next_page_token=cniej98234h84dn298d=
        /recipes?search=chicken
    """

    limit = request.args.get("limit", default=10, type=int)  # how many items to fetch
    if limit < 1 or limit > 100:
        return (
            jsonify(
                {
                    "error": {
                        "code": "INVALID_LIMIT",
                        "message": "limit must be between 1 and 100",
                    }
                }
            ),
            400,
        )
    next_page_token = request.args.get("next_page_token", type=str)

    search = request.args.get("search", default=None, type=str)

    last_id = None
    if next_page_token:
        try:
            decoded = base64.urlsafe_b64decode(next_page_token.encode()).decode()
            last_id = int(decoded)
        except Exception:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "INVALID_TOKEN",
                            "message": "Invalid next_page_token",
                        }
                    }
                ),
                400,
            )

    query = Recipe.query
    if search:
        query = query.filter(func.lower(Recipe.name).like(f"%{search.lower()}%"))
    if last_id:
        query = query.filter(Recipe.id > last_id)
    items = query.order_by(Recipe.id.asc()).limit(limit + 1).all()

    next_token = None
    if len(items) > limit:
        next_token = base64.urlsafe_b64encode(str(items[-1].id).encode()).decode()
        items = items[:-1]

    # total count only in the first page, to give idea to the client how many exist in the first page
    total = query.count() if not last_id else None

    # convert sqlalchemy objects
    recipes_data = [recipe.to_dict() for recipe in items]

    response = {"items": recipes_data, "limit": limit, "next_page_token": next_token}
    if total is not None:
        response["total"] = total

    return jsonify(response), 200


@api.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        return (
            jsonify({"error": {"code": "NOT FOUND", "message": "Recipe not found"}}),
            404,
        )
    return jsonify(recipe.to_dict()), 200


@api.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe_route(recipe_id):
    data = request.get_json()
    recipe = update_recipe(recipe_id, data)
    if not recipe:
        return (
            jsonify({"error": {"code": "NOT_FOUND", "message": "Recipe no found"}}),
            404,
        )
    return jsonify(recipe.to_dict()), 200


@api.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe_route(recipe_id):
    success = delete_recipe_service(recipe_id)
    if not success:
        return (
            jsonify({"error": {"code": "NOT_FOUND", "message": "Recipe not found"}}),
            404,
        )
    return f"The recipe with ID {recipe_id} is successfully deleted.", 200
