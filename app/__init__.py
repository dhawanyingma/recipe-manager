from flask import Flask, jsonify
from .api.routes import api
from .models.recipe import db

def create_app():
    app = Flask(__name__)

    #config 

    #Register Blueprints
    app.register_blueprint(api, url_prefix="/api/v1")

    #Root route 
    @app.route("/")
    def home():
        return jsonify({
            "message": "Welcome to the Recipe Manager API!",
            "status": "running",
            "endpoints": [
                "/api/v1/health",
                "/api/v1/version",
                "/api/v1/recipes"
            ]
        }), 200

    return app
