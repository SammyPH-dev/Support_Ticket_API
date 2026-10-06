from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token

authen_api = Blueprint("authen_api", __name__)

@authen_api.post('/authentification')
def authentification():
    donnees = request.get_json(silent=True)

    if donnees is None:
        return {
            "erreur": "Seulement un JSON est accepter"
        },400

    utilisateur = donnees.get("utilisateur")
    mot_de_passe = donnees.get("mot_de_passe")

    #Hardcoder pour le moment
    if (utilisateur != "admin" or mot_de_passe != "secret"):
        return {
            "erreur": "Identifiants invalides."
        }, 401

    jeton = create_access_token(identity=utilisateur)

    return {"jeton": jeton}, 200