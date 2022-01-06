from api import db
from api.account.models import Account
from api.account.schemas import account_schema
from api.note.models import Note
from api.note.schemas import note_schema, notes_schema


def truncate_db():
    meta = db.metadata
    for table in meta.sorted_tables[::-1]:
        db.session.execute(table.delete())
    db.session.commit()


def create_user(client):
    user_info = {
        "name": "John Doe",
        "email": "jdoe@gmail.com",
        "password": "123456789",
        "account_type": "normal",
    }
    client.post(
        "/api/account/",
        json=user_info,
    )
    return account_schema.dump(Account.query.filter_by(name=user_info["name"]))


def create_user_login_token(client):
    create_user(client)
    response = client.post(
        "/api/account/auth", json={"email": "jdoe@gmail.com", "password": "123456789"}
    )
    return response.json

def create_note(client, token):
    response = client.post(
        "/api/note/",
        json={"title": "Test Note 1", "content": "Test Note 1 content"},
        headers={"Authorization": f"Bearer {token}"},
    )
    note = note_schema.dump(Note.query.filter_by(title="Test Note 1").first())
    return note

def create_multiple_notes(client, token):
    for i in range(3):
        response = client.post(
            "/api/note/",
            json={"title": f"Test Note {i}", "content": f"Test Note {i} content"},
            headers={"Authorization": f"Bearer {token}"},
        )
    notes = notes_schema.dump(Note.query.all())
    return notes