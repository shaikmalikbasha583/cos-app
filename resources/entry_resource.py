from flask_restful import Resource
from models.entry import Entry


class EntryApi(Resource):
    def get(self):
        return {"entries": [Entry.json(entry) for entry in Entry.find_all()]}, 200
