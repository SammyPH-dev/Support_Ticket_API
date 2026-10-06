from getpass import getpass

import requests

URL_API = "http://127.0.0.1:5001"


class ClientTickets:
    def __init__(self, url_api: str):
        self.url_api = url_api
        self.session = requests.Session()

    def _envoyer_requete(
        self,
        methode: str,
        chemin: str,
        **options,
    ):
        try:
            reponse = self.session.request(
                methode,
                f"{self.url_api}{chemin}",
                timeout=5,
                **options,
            )
        except requests.RequestException as erreur:
            print(f"Impossible de contacter l'API : {erreur}")
            return None

        try:
            contenu = reponse.json()
        except ValueError:
            contenu = None

        if not reponse.ok:
            if isinstance(contenu, dict):
                message = contenu.get(
                    "erreur",
                    contenu.get("msg", reponse.text),
                )
            else:
                message = reponse.text

            print(f"Erreur HTTP {reponse.status_code} : {message}")
            return None

        return contenu

    def authentifier(
        self,
        utilisateur: str,
        mot_de_passe: str,
    ) -> bool:
        donnees = self._envoyer_requete(
            "POST",
            "/authentification",
            json={
                "utilisateur": utilisateur,
                "mot_de_passe": mot_de_passe,
            },
        )

        if not isinstance(donnees, dict):
            return False

        jeton = donnees.get("jeton")

        if not jeton:
            print("Aucun jeton reçu.")
            return False

        self.session.headers.update({
            "Authorization": f"Bearer {jeton}"
        })

        print("Authentification réussie.")
        return True

    def afficher_ticket(self, ticket: dict) -> None:
        print()
        print(f"Ticket #{ticket['id']}")
        print(f"Titre : {ticket['titre']}")
        print(f"Description : {ticket['description']}")
        print(f"Priorité : {ticket['priorite']}")
        print(f"Statut : {ticket['statut']}")
        print(f"Créé le : {ticket['date_creation']}")

    def afficher_tickets(self) -> None:
        tickets = self._envoyer_requete(
            "GET",
            "/ticket",
        )

        if tickets is None:
            return

        if not tickets:
            print("Aucun ticket.")
            return

        print(f"\nNombre de tickets : {len(tickets)}")

        for ticket in tickets:
            self.afficher_ticket(ticket)

    def afficher_ticket_par_id(self, ticket_id: int) -> None:
        ticket = self._envoyer_requete(
            "GET",
            f"/ticket/{ticket_id}",
        )

        if isinstance(ticket, dict):
            self.afficher_ticket(ticket)

    def creer_ticket(
        self,
        titre: str,
        description: str,
        priorite: str,
    ) -> None:
        ticket = self._envoyer_requete(
            "POST",
            "/ticket",
            json={
                "titre": titre,
                "description": description,
                "priorite": priorite,
            },
        )

        if isinstance(ticket, dict):
            print("Ticket créé avec succès.")
            self.afficher_ticket(ticket)

    def modifier_ticket(
        self,
        ticket_id: int,
        modifications: dict,
    ) -> None:
        ticket = self._envoyer_requete(
            "PUT",
            f"/ticket/{ticket_id}",
            json=modifications,
        )

        if isinstance(ticket, dict):
            print("Ticket modifié avec succès.")
            self.afficher_ticket(ticket)

    def supprimer_ticket(self, ticket_id: int) -> None:
        ticket = self._envoyer_requete(
            "DELETE",
            f"/ticket/{ticket_id}",
        )

        if isinstance(ticket, dict):
            print(
                f"Le ticket #{ticket['id']} a été supprimé."
            )


def demander_id() -> int | None:
    valeur = input("ID du ticket : ").strip()

    try:
        ticket_id = int(valeur)
    except ValueError:
        print("L'ID doit être un nombre entier.")
        return None

    if ticket_id <= 0:
        print("L'ID doit être supérieur à zéro.")
        return None

    return ticket_id


def afficher_menu() -> None:
    print()
    print("===== SERVICE DE SUPPORT =====")
    print("1 - Afficher tous les tickets")
    print("2 - Afficher un ticket")
    print("3 - Créer un ticket")
    print("4 - Modifier un ticket")
    print("5 - Supprimer un ticket")
    print("0 - Quitter")


def executer_menu(client: ClientTickets) -> None:
    while True:
        afficher_menu()
        choix = input("Choix : ").strip()

        if choix == "1":
            client.afficher_tickets()

        elif choix == "2":
            ticket_id = demander_id()

            if ticket_id is not None:
                client.afficher_ticket_par_id(ticket_id)

        elif choix == "3":
            titre = input("Titre : ")
            description = input("Description : ")
            priorite = input(
                "Priorité (BASSE, MOYENNE ou HAUTE) : "
            )

            client.creer_ticket(
                titre,
                description,
                priorite,
            )

        elif choix == "4":
            ticket_id = demander_id()

            if ticket_id is None:
                continue

            print(
                "Laissez un champ vide pour ne pas le modifier."
            )

            titre = input("Nouveau titre : ")
            description = input("Nouvelle description : ")
            priorite = input("Nouvelle priorité : ")
            statut = input("Nouveau statut : ")

            modifications = {}

            if titre.strip():
                modifications["titre"] = titre

            if description.strip():
                modifications["description"] = description

            if priorite.strip():
                modifications["priorite"] = priorite

            if statut.strip():
                modifications["statut"] = statut

            if not modifications:
                print("Aucune modification fournie.")
                continue

            client.modifier_ticket(
                ticket_id,
                modifications,
            )

        elif choix == "5":
            ticket_id = demander_id()

            if ticket_id is None:
                continue

            confirmation = input(
                f"Supprimer le ticket #{ticket_id}? (o/n) : "
            ).strip().lower()

            if confirmation == "o":
                client.supprimer_ticket(ticket_id)
            else:
                print("Suppression annulée.")

        elif choix == "0":
            print("Fermeture du client.")
            break

        else:
            print("Choix invalide.")


def main() -> None:
    client = ClientTickets(URL_API)

    print("===== AUTHENTIFICATION =====")
    utilisateur = input("Utilisateur : ")
    mot_de_passe = getpass("Mot de passe : ")

    if not client.authentifier(
        utilisateur,
        mot_de_passe,
    ):
        return

    executer_menu(client)


if __name__ == "__main__":
    main()