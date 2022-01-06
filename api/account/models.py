from marshmallow import Schema, fields, post_load
from werkzeug.security import generate_password_hash, check_password_hash
from api.extensions import db
import datetime

class Account(db.Model):
    __tablename__ = "cn_account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    password_hash = db.Column(db.String(120))
    account_type = db.Column(db.String(6), nullable=False, default="normal")
    
    @property
    def password(self):
        raise AttributeError("Password is a write-only field")

    @password.setter
    def password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()