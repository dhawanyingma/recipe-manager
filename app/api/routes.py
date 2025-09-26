from flask import Blueprint, jsonify

api = Blueprint("api", __name__)

@api.route("/health", methods = ["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@api.route("/version", methods = ["GET"])
def version():
    return jsonify({"version":"v1"}),200

