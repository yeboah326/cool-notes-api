from flask import Blueprint, request
from api.extensions import db
from api.tag.models import Tag, NoteTag
from api.tag.schemas import tag_schema, tags_schema
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

tag = Blueprint("tag",__name__, url_prefix="/api/tag")

@tag.post("/")
@jwt_required()
def tag_create():
    # Retrieve the incoming data
    data = request.get_json()
    data['author_id'] = get_jwt_identity()

    try:
        new_tag = tag_schema.load(data)

        db.session.add(new_tag)
        db.session.commit()
    except ValidationError as e:
        return {"message": "Invalid data", "errors": e.messages}, 422

    return {"message": f"{data['name']} created successfully"}, 200

@tag.delete("/<id>")
@jwt_required()
def tag_delete_by_id(id):
    # Retrieve the tag
    tag = Tag.find_by_id(id)

    if not tag:
        return {"message": "A tag with the given ID does not exist"}, 404

    db.session.delete(tag)
    db.session.commit()

    return {"message": "Tag deleted successfully"}, 200

@tag.put("/<id>")
@jwt_required()
def tag_update_by_id(id):
    """
    id
    new_name
    """
    # Retrieve the incoming data
    data = request.get_json()

    # Retrieve the tag
    tag = Tag.find_by_id(id)
    
    if not tag:
        return {"message": "A tag with the given ID does not exist"}, 404

    try:
        if data["new_name"]:
            tag.name = data["new_name"]
            db.session.commit()
    except KeyError:
        return {"message": "A new name was not provided for the tag"}, 422

    return {"message": "Tag updated successfully"}, 200


@tag.get("/<id>")
@jwt_required()
def tag_get_by_id(id):
    tag = tag_schema.dump(Tag.find_by_id(id))
    
    if not tag:
        return {"message": "A tag with the given ID does not exist"}, 404

    return {"tag": tag}, 200

@tag.get("/")
@jwt_required()
def tag_get_all():
    tags = tags_schema.dump(Tag.query.filter_by(author_id=get_jwt_identity()).all())
    return {"tags": tags}, 200

@tag.post("/add_tag")
@jwt_required()
def tag_add_to_note():
    """
    tag_id, note_id
    """
    # Retrieve the incoming data
    data = request.get_json()

    note_tag = NoteTag(note_id=data["note_id"],tag_id=data["tag_id"])
    db.session.add(note_tag)
    db.session.commit()

    return {"message": "Tag added to note successfully"}, 200


# TODO: Remove tag from note
@tag.post("/remove_tag")
@jwt_required()
def tag_remove_from_note():
    """
    tag_id, note_id
    """
    # Retrieve the incoming data
    data = request.get_json()
    db.session.query(NoteTag).filter_by(note_id=data["note_id"], tag_id=data["tag_id"]).delete()
    
    db.session.commit()

    return {"message": "Tag removed from note successfully"}, 200