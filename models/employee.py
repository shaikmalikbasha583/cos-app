from datetime import datetime

from flask_bcrypt import check_password_hash, generate_password_hash
from sqlalchemy.dialects.mysql import BIGINT, DATE, TEXT, TINYINT, VARCHAR

from db import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(VARCHAR(30), nullable=False)
    age = db.Column(TINYINT)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(TEXT)
    phone = db.Column(BIGINT)
    hire_date = db.Column(DATE)
    created_at = db.Column(db.DATETIME, default=datetime.now)

    def __init__(self, name, age, email, password, phone, hire_date):
        self.name = name
        self.age = age
        self.email = email
        self.password = password
        self.phone = phone
        self.hire_date = hire_date

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "hire_date": self.hire_date.strftime(r"%Y/%m/%d"),
            "created_at": self.created_at.strftime(r"%Y/%m/%d, %H:%M:%S"),
        }

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_emp_full_details(cls):
        sql = "SELECT e.id, e.name, e.age, e.email, e.password, e.phone, e.hire_date, e.created_at, c.card_number, r.name as role FROM employees e JOIN cards c ON e.id = c.emp_id JOIN employee_roles ON e.id = employee_roles.emp_id JOIN roles r ON employee_roles.role_id = r.id"
        return db.engine.execute(sql)

    @classmethod
    def get_card_number_by_emp_id(cls, emp_id):
        sql = f"SELECT card_number FROM cards c JOIN employees e ON c.emp_id = e.id WHERE e.id = {emp_id}"
        return db.engine.execute(sql)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_employee_ids(cls):
        sql = "SELECT id FROM employees"
        return db.engine.execute(sql)

    @classmethod
    def get_entries_by_employee(cls, id, year, month, day):
        sql = "SELECT e.time FROM `entries` e JOIN cards c ON e.card_number = c.card_number WHERE c.emp_id = {}".format(
            id
        )
        m_sql = ""
        checkin_query = checkout_query = ""
        if year != 0:
            sql = "{} AND YEAR(time) = {}".format(sql, year)
            m_sql = "{} AND YEAR(entries.time) = {}".format(m_sql, year)
        if month != 0:
            sql = "{} AND MONTH(time) = {}".format(sql, month)
            m_sql = "{} AND MONTH(entries.time) = {}".format(m_sql, month)
        if day != 0:
            sql = "{} AND DAY(time) = {}".format(sql, day)
            m_sql = "{} AND DAY(entries.time) = {}".format(m_sql, day)

        checkin_query = "{} AND type='IN' ORDER BY e.time ASC LIMIT 1 ".format(sql)
        checkout_query = "{} AND type='OUT' ORDER BY e.time DESC LIMIT 1 ".format(sql)

        query = f"SELECT emp.id, emp.name, date(entries.time) AS `Date`, (SELECT TIMEDIFF(({checkout_query}), ({checkin_query}))) AS `Hours` FROM employees emp JOIN cards ON cards.emp_id = emp.id JOIN entries ON entries.card_number = cards.card_number WHERE emp.id = {id} {m_sql} LIMIT 1"
        print(query)
        return db.engine.execute(query)

