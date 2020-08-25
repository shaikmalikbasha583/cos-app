from flask_restful import Resource, request
from flask_jwt_extended import create_access_token
from models.employee import Employee
from models.role import Role


class LoginApi(Resource):
    def post(self):

        body = request.get_json()
        email = body["email"]
        password = body["password"]

        if email is None:
            return {"msg": "email field is mandatory"}, 400
        if password is None:
            return {"msg": "password field is mandatory"}, 400

        emp = Employee.find_by_email(email)
        if not emp:
            return {"msg": f"employee not found with email: {email}."}, 404
        authorized = emp.check_password(password)
        if not authorized:
            return {"msg": f"wrong password"}, 401
        roles = []
        for row in Role.get_roles_by_emp_id(emp.json()["id"]):
            roles.append(row["name"])
        access_token = create_access_token(
            identity={"email": emp.email, "roles": roles}
        )
        return {"access_token": access_token, "roles": roles}, 200
