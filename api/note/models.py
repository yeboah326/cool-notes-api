from marshmallow import Schema, fields
import datetime
from api.account.models import Account
from api.extensions import db


class Note(db.Model):
    __tablename__ = "cn_note"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_on = db.Colum(db.DateTime, default=datetime.datetime.now)
    updated_on = db.Column(db.DateTime, onupdate=datetime.datetime.now)
    author_id = db.Column(db.Intger, db.ForeignKey("account.id", on_delete="cascade"), nullable=False)

    @property
    def author(self) -> str:
        return Account.find_by_id(self.author_id).name
    
    @property
    def date_created(self) -> str:
        return self.created_on.strftime("%Y-%m-%d")
    
    @property
    def date_updated(self) -> str:
        return self.date_updated.strftime("%Y-%m-%d")

class NoteSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=False)
    date_created =  fields.Date(dump_only=True)
    date_updated = fields.DateTime(dump_only=True)
