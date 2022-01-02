from flask import Blueprint
from api.note.models import Note

note = Blueprint("note",__name__, url_prefix="api/note/")

# TODO: Create blueprint with customized url prefix
# TODO: Create new note
# TODO: Modify existing note
# TODO: Delete existing note
# TODO: View all notes
# TODO: View single note
