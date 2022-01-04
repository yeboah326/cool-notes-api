from marshmallow import Schema, fields
import datetime
from api.account.models import Account
from api.tag.models import Tag, NoteTag
from api.extensions import db


class Note(db.Model):
    __tablename__ = "cn_note"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey("cn_account.id", ondelete="cascade"), nullable=False)

    @property
    def author(self) -> str:
        return Account.find_by_id(self.author_id).name
    
    @property
    def tags(self) -> str:
        note_tags = NoteTag.query.filter_by(note_id=self.id).all()
        tags = [Tag.find_by(note_tag.id) for note_tag in note_tags]
        return tags
    
    @classmethod
    def find_note_by_id(cls,id):
        return cls.query.filter_by(id=id).first()