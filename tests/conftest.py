import pytest

from app import creer_app
from app.dao import db


@pytest.fixture
def app(tmp_path):
    chemin_bd_test = tmp_path / "test.db"

    application = creer_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{chemin_bd_test}",
        "JWT_SECRET_KEY": "cle-test",
    })

    yield application

    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def entetes_authentification(client):
    reponse = client.post(
        "/authentification",
        json={
            "utilisateur": "admin",
            "mot_de_passe": "secret",
        },
    )

    jeton = reponse.get_json()["jeton"]

    return {
        "Authorization": f"Bearer {jeton}"
    }