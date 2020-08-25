from flask_restful import Resource, request
from models.role import Role


class RolesApi(Resource):
    def get(self):
        return {"roles": list(map(lambda role: role.json(), Role.find_all()))}, 200

    def post(self):
        body = request.get_json()
        role = Role(body["name"])
        try:
            role.save()
        except Exception as e:
            return (
                {
                    "msg": "Something went wrong while adding new role.",
                    "description": e,
                },
                500,
            )
        return {"msg": "New role added", "new_role": role.json()}, 201

