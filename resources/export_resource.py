from flask_restful import Resource
from flask import Response, stream_with_context
from models.employee import Employee
from flask_restful import Resource, request
from resources.employee_resource import get_entries
import csv
from io import StringIO
from security import manager_required


@stream_with_context
def generate(entries):
    data = StringIO()
    w = csv.writer(data)
    w.writerow(("Empd", "EmpName", "Date", "Hours"))
    yield data.getvalue()
    data.seek(0)
    data.truncate(0)

    for entry in entries:
        if isinstance(entry, list):
            for e in entry:
                print(dict(e))
                w.writerow((e["id"], e["name"], e["date"], e["hours"]))
        else:
            w.writerow((entry["id"], entry["name"], entry["date"], entry["hours"]))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)


class ExportEmployeeEntriesApi(Resource):
    @manager_required
    def get(self, id):
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
        entries = get_entries(id, year, month, day)
        response = Response(generate(entries))
        response.headers.set("Content-Disposition", "attachment", filename="export.csv")
        return response


class ExportEmployeesEntriesApi(Resource):
    @manager_required
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
        response = Response(generate(entries))
        response.headers.set("Content-Disposition", "attachment", filename="export.csv")
        return response
