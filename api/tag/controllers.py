from flask import Blueprint
from api.tag.models import Tag, NoteTag

tag = Blueprint("tag",__name__, url_prefix="api/tag/")

# TODO: Create blueprint with customized url prefix
# TODO: Create tag
# TODO: Delete tag
# TODO: Modify tag
# TODO: View single tag
# TODO: View all tags
# TODO: Add tag to note
# TODO: Remove tag from note