from marshmallow import Schema, fields
from api.account.models import Account
from api.extensions import db

class Tag(db.Model):
    __tablename__ = "cn_tag"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    author_id = db.Column(db.Intger, db.ForeignKey("account.id", on_delete="cascade"), nullable=False)

    @property
    def author(self):
        return Account.find_by_id(self.author_id).name

class TagSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True)
    date_created = fields.Date(required=True)


class NoteTags(db.Model):
    note_id = db.Column(db.Integer, db.ForeignKey("cn_note.id"), nullable=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("cn_tag.id"), nullabe=True)