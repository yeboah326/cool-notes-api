from marshmallow import Schema, fields 

class TagSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True)
    date_created = fields.Date(required=True, dump_only=True)

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

