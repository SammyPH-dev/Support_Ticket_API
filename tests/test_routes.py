def creer_ticket_test(client, entetes):
    return client.post(
        "/ticket",
        headers=entetes,
        json={
            "titre": "Écran défectueux",
            "description": "L'écran ne s'allume plus.",
            "priorite": "HAUTE",
        },
    )


#Test pour sante route
def test_sante(client):
    reponse = client.get("/sante")

    assert reponse.status_code == 200
    assert reponse.get_json() == {
        "disponible": "oui",
        "service": "Service de support ticket",
    }

#Test pour authentification route
def test_authentification_reussie(client):
    reponse = client.post(
        "/authentification",
        json={
            "utilisateur": "admin",
            "mot_de_passe": "secret",
        },
    )

    donnees = reponse.get_json()

    assert reponse.status_code == 200
    assert "jeton" in donnees


def test_authentification_refusee(client):
    reponse = client.post(
        "/authentification",
        json={
            "utilisateur": "admin",
            "mot_de_passe": "incorrect",
        },
    )

    assert reponse.status_code == 401
    assert reponse.get_json() == {
        "erreur": "Identifiants invalides."
    }

#Test pour voir si le jeton marche bien
def test_route_protegee_sans_jeton(client):
    reponse = client.get("/ticket")

    assert reponse.status_code == 401


def test_liste_vide_avec_jeton(
    client,
    entetes_authentification,
):
    reponse = client.get(
        "/ticket",
        headers=entetes_authentification,
    )

    assert reponse.status_code == 200
    assert reponse.get_json() == []

#Test CRUD
def test_creer_ticket(client, entetes_authentification):
    reponse = creer_ticket_test(
        client,
        entetes_authentification,
    )

    donnees = reponse.get_json()

    assert reponse.status_code == 201
    assert donnees["id"] is not None
    assert donnees["titre"] == "Écran défectueux"
    assert donnees["priorite"] == "HAUTE"
    assert donnees["statut"] == "OUVERT"
    assert donnees["date_creation"] is not None


def test_creation_priorite_invalide(
    client,
    entetes_authentification,
):
    reponse = client.post(
        "/ticket",
        headers=entetes_authentification,
        json={
            "titre": "Problème informatique",
            "description": "Description du problème.",
            "priorite": "URGENTE",
        },
    )

    assert reponse.status_code == 400
    assert "erreur" in reponse.get_json()


def test_obtenir_tous_les_tickets(
    client,
    entetes_authentification,
):
    creer_ticket_test(client, entetes_authentification)

    reponse = client.get(
        "/ticket",
        headers=entetes_authentification,
    )

    donnees = reponse.get_json()

    assert reponse.status_code == 200
    assert len(donnees) == 1
    assert donnees[0]["titre"] == "Écran défectueux"


def test_obtenir_ticket_par_id(
    client,
    entetes_authentification,
):
    creation = creer_ticket_test(
        client,
        entetes_authentification,
    )

    ticket_id = creation.get_json()["id"]

    reponse = client.get(
        f"/ticket/{ticket_id}",
        headers=entetes_authentification,
    )

    assert reponse.status_code == 200
    assert reponse.get_json()["id"] == ticket_id


def test_ticket_introuvable(
    client,
    entetes_authentification,
):
    reponse = client.get(
        "/ticket/9999",
        headers=entetes_authentification,
    )

    assert reponse.status_code == 404
    assert reponse.get_json() == {
        "erreur": "Le ticket demandé n'existe pas."
    }


def test_modifier_seulement_le_titre(
    client,
    entetes_authentification,
):
    creation = creer_ticket_test(
        client,
        entetes_authentification,
    )

    ticket_id = creation.get_json()["id"]

    reponse = client.put(
        f"/ticket/{ticket_id}",
        headers=entetes_authentification,
        json={
            "titre": "Écran principal défectueux"
        },
    )

    donnees = reponse.get_json()

    assert reponse.status_code == 200
    assert donnees["titre"] == "Écran principal défectueux"
    assert donnees["description"] == "L'écran ne s'allume plus."
    assert donnees["priorite"] == "HAUTE"
    assert donnees["statut"] == "OUVERT"


def test_modification_invalide(
    client,
    entetes_authentification,
):
    creation = creer_ticket_test(
        client,
        entetes_authentification,
    )

    ticket_id = creation.get_json()["id"]

    reponse = client.put(
        f"/ticket/{ticket_id}",
        headers=entetes_authentification,
        json={
            "statut": "INCONNU"
        },
    )

    assert reponse.status_code == 400
    assert "erreur" in reponse.get_json()


def test_supprimer_ticket(
    client,
    entetes_authentification,
):
    creation = creer_ticket_test(
        client,
        entetes_authentification,
    )

    ticket_id = creation.get_json()["id"]

    suppression = client.delete(
        f"/ticket/{ticket_id}",
        headers=entetes_authentification,
    )

    assert suppression.status_code == 200
    assert suppression.get_json()["id"] == ticket_id

    verification = client.get(
        f"/ticket/{ticket_id}",
        headers=entetes_authentification,
    )

    assert verification.status_code == 404