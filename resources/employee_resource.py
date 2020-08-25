import calendar
from datetime import datetime

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.employee import Employee
from models.entry import Entry
from security import manager_required


def get_entries(id, year, month, day):
    entries = []
    if day != 0:
        for row in Employee.get_entries_by_employee(id, year, month, day):
            entry = {
                "id": row[0],
                "name": row[1],
                "date": str(row[2]),
                "hours": str(row[3]),
            }
            entries.append(entry)
    else:
        for d in range(calendar.monthrange(year, month)[1]):
            for row in Employee.get_entries_by_employee(id, year, month, d + 1):
                entry = {
                    "id": row[0],
                    "name": row[1],
                    "date": str(row[2]),
                    "hours": str(row[3]),
                }
                entries.append(entry)
    return entries


class EmployeeApi(Resource):
    def get(self, id):
        emp = Employee.find_by_id(id)
        if emp is None:
            return (
                {
                    "msg": "not found",
                    "description": f"Employee with id {id} was not found.",
                },
                404,
            )
        return {"employee": emp.json()}, 200

    def delete(self, id):
        emp = Employee.find_by_id(id)
        if emp is None:
            return (
                {
                    "msg": "not found",
                    "description": f"Employee with id {id} was not found.",
                },
                404,
            )
        try:
            emp.remove()
        except Exception as e:
            return {"msg": "Something went wrong", "description": e}, 500
        return {"msg": "employee deleted successfully"}, 200


class EmployeeFullListApi(Resource):
    @manager_required
    def get(self):
        employees = []
        for row in Employee.get_emp_full_details():
            new_emp = {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "email": row[3],
                "password": row[4],
                "phone": row[5],
                "hire_date": row[6].strftime(r"%Y/%m/%d"),
                "created_at": row[7].strftime(r"%Y/%m/%d, %H:%M:%S"),
                "card_number": row[8],
                "role": row[9],
            }
            employees.append(new_emp)
        return (
            {"success": True, "employees": employees,},
            200,
        )


class EmployeeListApi(Resource):
    def get(self):
        return (
            {
                "success": True,
                "employees": [Employee.json(emp) for emp in Employee.find_all()],
            },
            200,
        )

    def post(self):
        body = request.get_json()
        hased_password = Employee.hash_password(body["password"])
        emp = Employee(
            body["name"],
            body["age"],
            body["email"],
            hased_password,
            body["phone"],
            datetime.strptime(body["hire_date"], r"%Y/%m/%d"),
        )
        try:
            emp.save()
        except Exception as e:
            return {"msg": "Something went wrong", "description": e}, 500
        if emp.json()["id"] != None:
            return {"msg": "New Employee created.", "created_employee": emp.json()}, 201
        return {"msg": "Something went wrong"}, 500


class EmployeeListWithEntriesApi(Resource):
    def get(self, id):
        year = request.args.get("year")
        month = request.args.get("month")
        day = request.args.get("day")

        if year is None:
            return Response({"msg", "Please provide the year in the query param."}), 400
        else:
            year = int(year) if len(year) > 0 else 0
        if month is None:
            return (
                Response({"msg", "Please provide the month in the query param."}),
                400,
            )
        else:
            month = int(month) if len(month) > 0 else 0
        if day is None:
            day = 0
        else:
            day = int(day) if len(day) > 0 else 0

        entries = get_entries(id, year, month, day)
        return {"entries": entries}, 200


class EmployeesListWithEntriesApi(Resource):
    def get(self):
        year = request.args.get("year")
        month = request.args.get("month")
        day = request.args.get("day")
        if year is None:
            return {"msg", "Please provide the year in the query param."}, 400
        else:
            year = int(year) if len(year) > 0 else 0
        if month is None:
            return (
                {"msg", "Please provide the month in the query param."},
                400,
            )
        else:
            month = int(month) if len(month) > 0 else 0
        if day is None:
            day = 0
        else:
            day = int(day) if len(day) > 0 else 0
        entries = []
        employee_ids = [row["id"] for row in Employee.get_employee_ids()]
        for _id in employee_ids:
            emp_entries = get_entries(_id, year, month, day)
            if len(emp_entries) > 0:
                entries.append(emp_entries)
        return {"entries": entries}, 200
