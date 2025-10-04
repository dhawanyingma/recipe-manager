from flask import Blueprint, jsonify, request
from app.services.recipe_service import create_recipe, get_all_recipes, get_recipe_by_id, update_recipe, delete_recipe_service, validate_recipe_data

api = Blueprint("api", __name__)

@api.route("/health", methods = ["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@api.route("/version", methods = ["GET"])
def version():
    return jsonify({"version":"v1"}),200

@api.route("/recipes", methods=["POST"])
def create_recipe_route():
    data = request.get_json() or {}
    print(data)
    errors = validate_recipe_data(data)
    print(errors)
    if errors:
        return jsonify({
            "errors" : "VALIDATION_ERROR",
            "message" : "Invalid request data",
            "details" : errors
        }), 400
    recipe = create_recipe(data)
    return jsonify({"id":recipe.id, "name":recipe.name}), 201

@api.route("/recipes", methods = ["GET"])
def get_recipes_route():
    recipes = get_all_recipes()
    return jsonify([recipe.to_dict() for recipe in recipes]), 200

@api.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        return jsonify({
            "error" : {
                "code" : "NOT FOUND",
                "message" : "Recipe not found"
            }
        }), 404
    return jsonify(recipe.to_dict()), 200

@api.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe_route(recipe_id):
    data = request.get_json()
    recipe = update_recipe(recipe_id, data)
    if not recipe:
        return jsonify({
            "error":{
                "code" : "NOT_FOUND",
                "message" : "Recipe no found"
            } 
        }), 404
    return jsonify(recipe.to_dict()), 200

@api.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe_route(recipe_id):
    success = delete_recipe_service(recipe_id)
    if not success:
        return jsonify({
            "error" : {
                "code" : "NOT_FOUND",
                "message" : "Recipe not found"
            }
        }), 404
    return f"The recipe with ID {recipe_id} is successfully deleted.",200
    


