from flask import Blueprint, request
from api.extensions import db
from api.note.models import Note
from api.note.schemas import note_schema, notes_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError

note = Blueprint("note",__name__, url_prefix="/api/note")

@note.post("/")
@jwt_required()
def note_create():
    # Retrieve the incoming data
    data = request.get_json()
    data["author_id"] = get_jwt_identity()

    try:
        # Create a new note instance
        new_note = note_schema.load(data)
        
        # Add to the database
        db.session.add(new_note)
        db.session.commit()

        return {"message": "Note created successfully"}, 200
    
    except ValidationError as e:
        return {"messages": "Invalid data", "errors": e.messages}, 400

@note.put("/<id>")
@jwt_required()
def note_update_by_id(id):
    data = request.get_json()

    note = Note.find_note_by_id(id)
    if not note:
        return {"message": "A note with the given ID does not exist"}, 404
    
    # Update the note
    try:
        note.title = data['new_title']
    except KeyError:
        pass
    try:
        note.content = data['new_content']
    except KeyError:
        pass

    # Save the changes made
    db.session.commit()

    return {"message": "Note updated successfully"}, 200
    
@note.delete("/<id>")
@jwt_required()
def note_delete_by_id(id):
    # Retrieve the note
    note = Note.find_note_by_id(id)

    if not note:
        return {"message": "A note with the given ID does not exist"}, 404

    # Delete the note
    db.session.delete(note)
    db.session.commit()

    return {"message": "Note deleted successfully"}, 200

@note.delete("/")
@jwt_required()
def note_delete_by_all():
    # Retrieve the note
    note = Note.find_note_by_id(id)

    if not note:
        return {"message": "A note with the given ID does not exist"}, 404

    # Delete the note
    db.session.delete(note)
    db.session.commit()

    return {"message": "Note deleted successfully"}, 200


@note.get("/")
@jwt_required()
def note_get_all():
    # Get all the notes created by the user
    notes = notes_schema.dump(Note.query.filter_by(author_id=get_jwt_identity()))
    return {"notes": notes}, 200

@note.get("/<id>")
@jwt_required()
def note_get_by_id(id):
    note = note_schema.dump(Note.find_note_by_id(id))
    
    if not note:
        return {"message": "A note with the given ID does not exist"}, 404
    
    return {"note": note}, 200