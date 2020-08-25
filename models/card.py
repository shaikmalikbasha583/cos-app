from db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime


class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.INTEGER, primary_key=True)
    card_number = db.Column(BIGINT, nullable=False, unique=True)
    emp_id = db.Column(db.INTEGER)

    def __init__(self, card_number, emp_id):
        self.card_number = card_number
        self.emp_id = emp_id

    def json(self):
        return {"id": self.id, "card_number": self.card_number, "emp_id": self.emp_id}

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()
