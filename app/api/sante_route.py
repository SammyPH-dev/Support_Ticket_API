from flask import Blueprint, jsonify

sante_api = Blueprint("sante_api", __name__)

@sante_api.get("/")
def index():
    return jsonify({
        "message": "Sante API",
    }), 200

@sante_api.get("/sante")
def sante():
    return jsonify({
        "disponible": "oui",
        "service": "Service de support ticket"
            }), 200