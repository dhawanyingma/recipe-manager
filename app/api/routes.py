from flask import Blueprint, jsonify, request
from app.services.recipe_service import create_recipe, get_all_recipes

api = Blueprint("api", __name__)

@api.route("/health", methods = ["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@api.route("/version", methods = ["GET"])
def version():
    return jsonify({"version":"v1"}),200

@api.route("/recipes", methods=["POST"])
def create_recipe_route():
    data = request.get_json()
    recipe = create_recipe(data)
    return jsonify({"id":recipe.id, "name":recipe.name}), 201

@api.route("/recipes", methods = ["GET"])
def get_recipes_route():
    recipes = get_all_recipes()
    return jsonify([
        {
            "id" : recipe.id,
            "name" : recipe.name,
            "ingredients" : recipe.ingredients,
            "tags" : recipe.tags,
            "created_at" : recipe.created_at,
            "updated_at" :recipe.updated_at
         } for recipe in recipes
    ]), 200


