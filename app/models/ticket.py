from app.dao import db

#Un exemple de comment un ticket va ressembler
exemple = {
  "id": 1,
  "titre": "Écran défectueux",
  "description": "L'écran du poste 14 ne s'allume plus.",
  "priorite": "HAUTE",
  "statut": "OUVERT",
  "date_creation": "2026-10-05T14:30:00"
}

class Ticket(db.Model):
    __tablename__ = "ticket"

    id = db.Column(db.Integer, primary_key=True)

    titre = db.Column(db.String(100), nullable=False)

    description = db.Column(db.String(10000))

    priorite = db.Column(db.String(100), nullable=False)

    statut = db.Column(db.String(100), nullable=False)

    date_creation = db.Column(db.DateTime)

    def retourne_ticket(self):
        return {
            "id": self.id,
            "titre": self.titre,
            "description": self.description,
            "priorite": self.priorite,
            "statut": self.statut,
            "date_creation": (
            self.date_creation.isoformat()
            if self.date_creation is not None
            else None
        )
        }