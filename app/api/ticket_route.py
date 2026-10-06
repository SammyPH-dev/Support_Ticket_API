from flask import Blueprint, jsonify, request
from app.dao.ticket_dao import TicketDao
from app.services.ticket_service import TicketService
from flask_jwt_extended import jwt_required

ticket_api = Blueprint('ticket_api', __name__)

ticket_service = TicketService(TicketDao())

@ticket_api.get('/ticket/<int:ticket_id>')
@jwt_required()
def get_ticket(ticket_id: int) -> dict:
    ticket = ticket_service.obtenir_ticket(ticket_id)

    if ticket is None:
        return jsonify({
            "erreur": "Le ticket demandé n'existe pas."
        }), 404

    return jsonify(ticket.retourne_ticket()), 200

@ticket_api.get('/ticket')
@jwt_required()
def get_all_tickets() -> list:
    tickets = ticket_service.obtenir_tout_ticket()

    resultat = [
        ticket.retourne_ticket()
        for ticket in tickets
    ]

    return jsonify(resultat), 200


@ticket_api.post('/ticket')
@jwt_required()
def post_ticket():
    donnees = request.get_json(silent=True)

    if not isinstance(donnees, dict):
        return jsonify({
            "erreur": "Le corps de la requête doit contenir du JSON."
        }), 400

    try:
        ticket = ticket_service.creer_ticket(donnees)
    except ValueError as erreur:
        return jsonify({
            "erreur": str(erreur)
        }), 400

    return jsonify(ticket.retourne_ticket()), 201


@ticket_api.put('/ticket/<int:ticket_id>')
@jwt_required()
def put_ticket(ticket_id: int) -> dict:
    donnees = request.get_json(silent=True)
    ticket = ticket_service.obtenir_ticket(ticket_id)

    if not isinstance(donnees, dict):
        return jsonify({
            "erreur": "Le corps de la requête doit contenir du JSON."
        }), 400

    if ticket is None:
        return jsonify({
            "erreur": "Le ticket demandé n'existe pas."
        }), 404

    try:
        ticket = ticket_service.modifier_ticket(ticket, donnees)
    except ValueError as erreur:
        return jsonify({
            "erreur": str(erreur)
        }), 400
    return jsonify(ticket.retourne_ticket()), 200

@ticket_api.delete('/ticket/<int:ticket_id>')
@jwt_required()
def delete_ticket(ticket_id: int) -> dict:
    ticket = ticket_service.obtenir_ticket(ticket_id)

    if ticket is None:
        return jsonify({
            "erreur": "Le ticket demandé n'existe pas."
        }), 404

    ticket = ticket_service.enlever_ticket(ticket)

    return jsonify(ticket.retourne_ticket()), 200