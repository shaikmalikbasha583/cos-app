from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

from resources.auth import LoginApi
from resources.card_resource import CardListApi
from resources.employee_resource import (
    EmployeeApi,
    EmployeeFullListApi,
    EmployeeListApi,
    EmployeeListWithEntriesApi,
    EmployeesListWithEntriesApi,
)
from resources.employee_role_resource import EmployeeRolesApi
from resources.entry_resource import EntryApi
from resources.role_resource import RolesApi
from resources.export_resource import (
    ExportEmployeeEntriesApi,
    ExportEmployeesEntriesApi,
)

app = Flask(__name__)
app.config["DEBUG"] = True

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://costrategix:costrategix@localhost:3306/cos_app_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["JWT_SECRET_KEY"] = "thisissupersecretkey"

CORS(app)

api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_schema():
    db.create_all()


@jwt.user_claims_loader
def adding_roles(employee):
    return {"roles": employee["roles"]}


api.add_resource(EmployeeListApi, "/employees")  # create and get the employees
api.add_resource(CardListApi, "/cards")  # create and get the cards for employees

api.add_resource(EmployeesListWithEntriesApi, "/employees/entries")
api.add_resource(EmployeeListWithEntriesApi, "/employees/<int:id>/entries")

api.add_resource(ExportEmployeesEntriesApi, "/export/employees/entries")
api.add_resource(ExportEmployeeEntriesApi, "/export/employees/<int:id>/entries")

api.add_resource(EmployeeFullListApi, "/employees/all")
api.add_resource(EmployeeApi, "/employee/<int:id>")

api.add_resource(RolesApi, "/roles")
api.add_resource(EmployeeRolesApi, "/employee/roles")

api.add_resource(EntryApi, "/entries")
api.add_resource(LoginApi, "/login")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(host="localhost", port=5000)
