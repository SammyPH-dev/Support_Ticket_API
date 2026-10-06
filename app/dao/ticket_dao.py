from app.dao import db
from app.models import Ticket

class TicketDao:

    def get_ticket(self, ticket_id: int) -> Ticket:
        return db.session.get(Ticket, ticket_id)

    def get_all_tickets(self) -> list[Ticket]:
        query = db.select(Ticket)
        return list(db.session.scalars(query))

    def create_ticket(self, ticket: Ticket) -> Ticket | None:
        try:
            db.session.add(ticket)
            db.session.commit()
            db.session.refresh(ticket)
            return ticket
        except Exception:
            db.session.rollback()
            raise

    def modify_ticket(self, ticket: Ticket) -> Ticket | None:
        try:
            db.session.merge(ticket)
            db.session.commit()
            return ticket
        except Exception:
            db.session.rollback()
            raise

    def remove_ticket(self, ticket: Ticket) -> Ticket | None:
        try:
            db.session.delete(ticket)
            db.session.commit()
            return ticket
        except Exception:
            db.session.rollback()
            raise


