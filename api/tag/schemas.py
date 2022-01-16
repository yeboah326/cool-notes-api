from marshmallow import Schema, fields, post_load
from api.tag.models import Tag

class TagSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True)
    author_id = fields.Int(required=True)
    date_created = fields.Date(required=True, dump_only=True)

    @post_load
    def create_tag(self, data, **kwargs):
        return Tag(**data)

tag_schema = TagSchema(unknown="EXCLUDE")
tags_schema = TagSchema(many=True, unknown="EXCLUDE")

