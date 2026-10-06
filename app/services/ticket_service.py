from datetime import datetime, timezone

from app.dao.ticket_dao import TicketDao
from app.models import Ticket


class TicketService:
    def __init__(self, dao: TicketDao):
        self.dao = dao

    def _verifier_donnees(self, donnees: dict, modification: bool = False) -> dict:
        resultat = {}

        # Le titre est obligatoire à la création,
        # mais facultatif pendant une modification.
        if not modification or "titre" in donnees:
            titre = donnees.get("titre")

            if not isinstance(titre, str) or not titre.strip():
                raise ValueError("Le titre est obligatoire.")

            resultat["titre"] = titre.strip()

        # La description est facultative à la création.
        if not modification or "description" in donnees:
            description = donnees.get("description", "")

            if not isinstance(description, str):
                raise ValueError("La description doit être une chaîne de caractères.")

            resultat["description"] = description.strip()

        # La priorité est obligatoire à la création.
        if not modification or "priorite" in donnees:
            priorite = donnees.get("priorite")

            if not isinstance(priorite, str):
                raise ValueError("La priorité est obligatoire.")

            priorite = priorite.upper()

            if priorite not in {"BASSE", "MOYENNE", "HAUTE"}:
                raise ValueError("La priorité doit être BASSE, MOYENNE ou HAUTE.")

            resultat["priorite"] = priorite

        # Le statut peut seulement être fourni pendant une modification.
        if modification and "statut" in donnees:
            statut = donnees.get("statut")

            if not isinstance(statut, str):
                raise ValueError("Le statut doit être une chaîne de caractères.")

            statut = statut.upper()

            if statut not in {"OUVERT", "EN_COURS", "RESOLU"}:
                raise ValueError("Le statut doit être OUVERT, EN_COURS ou RESOLU.")

            resultat["statut"] = statut

        if modification and not resultat:
            raise ValueError("Aucun champ modifiable n'a été fourni.")

        return resultat

    def obtenir_ticket(self, ticket_id: int) -> Ticket:
        return self.dao.get_ticket(ticket_id)

    def obtenir_tout_ticket(self) -> list[Ticket]:
        return self.dao.get_all_tickets()

    def creer_ticket(self, donnees: dict) -> Ticket:
        donnees_valides = self._verifier_donnees(donnees)

        ticket = Ticket(
            titre=donnees_valides["titre"],
            description=donnees_valides["description"],
            priorite=donnees_valides["priorite"],
            statut="OUVERT",
            date_creation=datetime.now(timezone.utc),
        )

        return self.dao.create_ticket(ticket)

    def modifier_ticket(self, ticket: Ticket, donnees: dict) -> Ticket:
        modifications = self._verifier_donnees(
            donnees,
            modification=True,
        )

        for key, value in modifications.items():
            setattr(ticket, key, value)

        return self.dao.modify_ticket(ticket)

    def enlever_ticket(self, ticket: Ticket) -> Ticket:
        return self.dao.remove_ticket(ticket)