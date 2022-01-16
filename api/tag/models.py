import datetime
from api.account.models import Account
from api.extensions import db

class Tag(db.Model):
    __tablename__ = "cn_tag"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey("cn_account.id", ondelete="cascade"), nullable=False)

    @property
    def author(self):
        return Account.find_by_id(self.author_id).name

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
class NoteTag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, db.ForeignKey("cn_note.id"), nullable=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("cn_tag.id"), nullable=True)

    @classmethod
    def find_note_tag(cls, note_id, tag_id):
        return cls.query.filter_by(note_id=note_id, tag_id=tag_id)