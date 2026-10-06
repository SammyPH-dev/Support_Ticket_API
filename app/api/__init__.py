from flask import Blueprint, Flask
from app.api.sante_route import sante_api
from app.api.ticket_route import ticket_api
from app.api.authen_route import authen_api


def enregistrer_api(app: Flask) -> None:
    app.register_blueprint(sante_api)
    app.register_blueprint(ticket_api)
    app.register_blueprint(authen_api)
