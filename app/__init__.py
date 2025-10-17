from flask import Flask, jsonify
from .api.routes import api
from app.db import db
from app import models
from flask_migrate import Migrate
from .errors import register_error_handlers
from app.LogUtil import LogUtil
import logging   # ✅ Add this

migrate = Migrate()

def create_app(config_class="config.DevConfig"):  # devconfig as default
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ✅ Disable noisy Werkzeug access logs
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    # Initialize DB + migrations
    db.init_app(app)
    migrate.init_app(app, db)

    print("DEBUG MODE", app.debug)

    # Register Blueprints
    app.register_blueprint(api, url_prefix="/api/v1")

    # Initialize centralized logging
    LogUtil.init_app(app)

    # Root route
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

    register_error_handlers(app)
    return app
