from api import db
from api.account.models import Account
from api.account.schemas import account_schema
from api.note.models import Note
from api.note.schemas import note_schema, notes_schema
from api.tag.models import NoteTag, Tag
from api.tag.schemas import tag_schema, tags_schema


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
        json={"note":{"title": "Test Note 1", "content": "Test Note 1 content"}, "tags":[{"name":"cool"}, {"name":"new"}]},
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


def create_tag(client, user):
    client.post(
        "/api/tag/",
        json={"name": "food"},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    tag = tag_schema.dump(Tag.query.filter_by(name="food").first())

    return tag


def create_multiple_tags(client, user):
    for i in range(3):
        client.post(
            "/api/tag/",
            json={"name": f"food{i}"},
            headers={"Authorization": f"Bearer {user['token']}"},
        )

    tags = tags_schema.dump(Tag.query.filter_by(author_id=user["account"]["id"]))

    return tags


def create_note_with_tag(client, user):
    # Create a tag for testing
    tag = create_tag(client, user)

    # Create a new note for testing
    note = create_note(client, user["token"])

    response = client.post(
        "api/tag/add_tag",
        json={"note_id": note["id"], "tag_id": tag["id"]},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    note_tag = NoteTag.query.filter_by(note_id=note["id"], tag_id=tag["id"]).first()

    return note_tag
