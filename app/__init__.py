from pathlib import Path
from app.api import enregistrer_api
from app.dao import db
from flask import Flask
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def creer_app(configuration: dict | None = None):
    app = Flask(__name__)

    racine_projet = Path(__file__).resolve().parent.parent

    chemin_bd = racine_projet / "data" / "ticket.db"

    chemin_bd.parent.mkdir(parents=True, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = (f"sqlite:///{chemin_bd}")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = ("cle-secrete")

    if configuration is not None:
        app.config.update(configuration)

    db.init_app(app)
    jwt.init_app(app)

    enregistrer_api(app)

    with app.app_context():
        from app.models import ticket
        db.create_all()

    return app
