from db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mysql import VARCHAR
from datetime import datetime


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(VARCHAR(30), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"id": self.id, "name": self.name}

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def get_roles_by_emp_id(cls, id):
        sql = "SELECT r.name FROM roles r JOIN employee_roles er ON r.id = er.role_id JOIN employees e ON er.emp_id = e.id WHERE e.id = {}".format(
            id
        )
        return db.engine.execute(sql)

