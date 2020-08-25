from db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, ENUM
from datetime import datetime


class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.INTEGER, primary_key=True)
    card_number = db.Column(BIGINT, nullable=False)
    type = db.Column(ENUM("IN", "OUT"))
    time = db.Column(DATETIME, default=datetime.now)

    def __init__(self, card_number, type):
        self.card_number = card_number
        self.type = type

    def json(self):
        return {
            "id": self.id,
            "card_number": self.card_number,
            "type": self.type,
            "time": self.time.strftime(r"%Y/%m/%d, %H:%M:%S"),
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def get_entries_by_emp_id(cls, emp_id, year, month, day):
        year = int(year) if len(year) > 0 else 0
        month = int(month) if len(month) > 0 else 0
        day = int(day) if len(day) > 0 else 0
        sql = text(f"SELECT * FROM entries WHERE emp_id = {emp_id}")
        if year != 0:
            sql = " {} AND YEAR(time) = {}".format(sql, year)
        if month != 0:
            sql = " {} AND MONTH(time) = {}".format(sql, month)
        if day != 0:
            sql = " {} AND DAY(time) = {}".format(sql, day)

        return db.engine.execute(sql)
