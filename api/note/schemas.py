from api.note.models import Note
from marshmallow import Schema, fields, post_load

class NoteSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=False)
    author_id = fields.Int(required=True, load_only=True)
    author = fields.Str(required=True, dump_only=True)
    date_created =  fields.Date(dump_only=True)
    date_updated = fields.DateTime(dump_only=True)
    tags = fields.List(fields.Str,allow_none=True, dump_only=True)

    @post_load
    def create_note(self, data, **kwargs):
        return Note(**data)

note_schema = NoteSchema(unknown="EXCLUDE")
notes_schema = NoteSchema(many=True)