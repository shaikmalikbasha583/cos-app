from models.card import Card
from flask_restful import Resource, request


class CardListApi(Resource):
    def post(self):
        body = request.get_json()
        card = Card(body["card_number"], body["emp_id"])
        try:
            card.save()
        except Exception as e:
            return (
                {
                    "msg": "Something went wrong while adding access card to db.",
                    "description": e,
                },
                500,
            )
        return {"msg": "New card created for employee.", "card": card.json()}, 201

    def get(self):
        return {"cards": list(map(lambda card: card.json(), Card.find_all()))}, 200
