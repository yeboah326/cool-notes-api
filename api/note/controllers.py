from flask import Blueprint
from api.note.models import Note
from flask_jwt_extended import jwt_required

note = Blueprint("note",__name__, url_prefix="api/note")

# TODO: Create new note
@note.post("/")
@jwt_required()
def note_create():
    pass

# TODO: Modify existing note
@note.put("/<id>")
@jwt_required()
def note_update_by_id(id):
    pass

# TODO: Delete existing note
@note.put("/<id>")
@jwt_required()
def note_delete_by_id(id):
    pass



# TODO: View all notes
@note.get("/")
@jwt_required()
def note_view_all():
    pass


# TODO: View single note
@note.get("/<id>")
@jwt_required()
def note_view_by_id(id):
    pass