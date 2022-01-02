from flask import Blueprint
from api.tag.models import Tag, NoteTag
from flask_jwt_extended import jwt_required

tag = Blueprint("tag",__name__, url_prefix="api/tag")

# TODO: Create tag
@tag.post("/")
def tag_create():
    pass

# TODO: Delete tag
@tag.delete("/id")
@jwt_required()
def tag_delete_by_id(id):
    pass

# TODO: Modify tag
@tag.put("/id")
@jwt_required()
def tag_update_by_id(id):
    pass

# TODO: View single tag
@tag.get("/<id>")
@jwt_required()
def tag_get_by_id(id):
    pass

# TODO: View all tags
@tag.get("/")
@jwt_required()
def tag_view_all():
    pass

# TODO: Add tag to note
@tag.post("/add_tag")
@jwt_required()
def tag_add_to_note():
    pass

# TODO: Remove tag from note
@tag.post("/remove_tag")
@jwt_required()
def tag_remove_from_note():
    pass