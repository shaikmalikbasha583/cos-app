from db import db


class EmployeeRoles(db.Model):
    __tablename__ = "employee_roles"

    id = db.Column(db.INTEGER, primary_key=True)
    emp_id = db.Column(db.INTEGER, nullable=False)
    role_id = db.Column(db.INTEGER, nullable=False)

    def __init__(self, emp_id, role_id):
        self.emp_id = emp_id
        self.role_id = role_id

    def json(self):
        return {"id": self.id, "emp_id": self.emp_id, "role_id": self.role_id}

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

