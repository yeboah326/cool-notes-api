from marshmallow import Schema, fields

class NoteSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=False)
    date_created =  fields.Date(dump_only=True)
    date_updated = fields.DateTime(dump_only=True)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)