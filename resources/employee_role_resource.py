from flask_restful import Resource, request
from models.employee_role import EmployeeRoles


class EmployeeRolesApi(Resource):
    def get(self):
        return (
            {
                "employee_roles": list(
                    map(lambda emp: emp.json(), EmployeeRoles.find_all())
                )
            },
            200,
        )

    def post(self):
        body = request.get_json()
        emp_roles = EmployeeRoles(body["emp_id"], body["role_id"])
        try:
            emp_roles.save()
        except Exception as e:
            return {"msg": "something went wrong", "description": e}, 500
        return (
            {
                "msg": f"New role added to employee{body['emp_id']}",
                "created_role": emp_roles.json(),
            },
            201,
        )
