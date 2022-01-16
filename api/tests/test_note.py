from api.tests.setup import *
from api.note.models import Note
from api.note.schemas import note_schema


def test_note_create_successful(client):
    # Truncate all database tables
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    response = client.post(
        "/api/note/",
        json={"note":{"title": "Test Note 1", "content": "Test Note 1 content"}, "tags":[{"name":"cool"}, {"name":"new"}]},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    note = note_schema.dump(Note.query.filter_by(title="Test Note 1").first())

    assert response.status_code == 200
    assert response.json["message"] == "Note created successfully"
    assert note["content"] == "Test Note 1 content"
    assert note["title"] == "Test Note 1"
    assert note["author"] == "John Doe"
    assert len(note["tags"]) == 2

    # Truncate all database tables
    truncate_db()


def test_note_create_error(client):
    # Truncate all database tables
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    response = client.post(
        "/api/note/",
        json={"content": "Test Note 1 content"},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    # Try to retrieve note instance
    note = note_schema.dump(Note.query.filter_by(title="Test Note 1").first())

    assert response.status_code == 422
    assert response.json["errors"] == {"title": ["Missing data for required field."]}
    assert response.json["messages"] == "Invalid data"
    assert note == {}
    # Truncate all database tables
    truncate_db()


def test_note_update_by_id_successful(client):
    # Truncate all database tables
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a new note for testing
    note = create_note(client, user["token"])

    response = client.put(
        f"/api/note/{note['id']}",
        json={"new_title": "New title 1", "new_content": "New content 1"},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    # Retrieve the modified note
    modified_note = note_schema.dump(Note.find_note_by_id(id=note["id"]))

    assert response.status_code == 200
    assert response.json["message"] == "Note updated successfully"
    assert modified_note["title"] == "New title 1"
    assert modified_note["content"] == "New content 1"

    # Truncate all database tables
    truncate_db()


def test_note_update_by_id_non_exist(client):
    # Truncate all database tables
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a new note for testing
    note = create_note(client, user["token"])

    response = client.put(
        f"/api/note/{note['id'] + 1}",
        json={"new_title": "New title 1", "new_content": "New content 1"},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    # Retrieve the modified note
    modified_note = note_schema.dump(Note.find_note_by_id(id=note["id"] + 1))

    assert response.status_code == 404
    assert response.json["message"] == "A note with the given ID does not exist"
    assert modified_note == {}

    # Truncate all database tables
    truncate_db()


def test_note_delete_by_id_successful(client):
    # Truncate all database tables
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a new note for testing
    note = create_note(client, user["token"])

    response = client.delete(
        f"/api/note/{note['id']}", headers={"Authorization": f"Bearer {user['token']}"}
    )

    # Retrieve the deleted note
    deleted_note = note_schema.dump(Note.find_note_by_id(id=note["id"] + 1))

    assert response.status_code == 200
    assert response.json["message"] == "Note deleted successfully"
    assert deleted_note == {}

    # Truncate all database tables
    truncate_db()


def test_note_delete_by_id_non_exist(client):
    # Truncate all database tables
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a new note for testing
    note = create_note(client, user["token"])

    response = client.delete(
        f"/api/note/{note['id'] + 1}",
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "A note with the given ID does not exist"

    # Truncate all database tables
    truncate_db()


def test_note_delete_all_successful(client):
    # Truncate all database tables
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create multiple notes for testing
    notes = create_multiple_notes(client, user["token"])

    response = client.delete(
        "api/note/", headers={"Authorization": f"Bearer {user['token']}"}
    )

    # Get all the notes created by the current user
    notes = notes_schema.dump(Note.query.filter_by(author_id=user["account"]["id"]))

    assert response.status_code == 200
    assert response.json["message"] == "Notes deleted successfully"
    assert notes == []

    # Truncate all database tables
    truncate_db()


def test_note_get_all_successful(client):
    # Truncate all database tables
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create multiple notes for testing
    notes = create_multiple_notes(client, user["token"])

    response = client.get(
        "api/note/", headers={"Authorization": f"Bearer {user['token']}"}
    )

    # Get all the notes created by the current user
    notes = notes_schema.dump(Note.query.filter_by(author_id=user["account"]["id"]))

    assert response.status_code == 200
    assert len(response.json["notes"]) == 3
    assert response.json["notes"][0]["title"] == "Test Note 0"
    assert response.json["notes"][1]["title"] == "Test Note 1"
    assert response.json["notes"][2]["title"] == "Test Note 2"

    # Truncate all database tables
    truncate_db()


def test_note_get_by_id_successful(client):
    # Truncate all database tables
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a new note for testing
    note = create_note(client, user["token"])

    response = client.get(
        f"/api/note/{note['id']}",
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    note = note_schema.dump(Note.query.filter_by(title="Test Note 1").first())

    assert response.status_code == 200
    assert response.json["note"]["title"] == "Test Note 1"
    assert response.json["note"]["content"] == "Test Note 1 content"

    # Truncate all database tables
    truncate_db()


def test_note_by_id_non_exist(client):
    # Truncate all database tables
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a new note for testing
    note = create_note(client, user["token"])

    response = client.get(
        f"/api/note/{note['id'] + 1}",
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    assert response.status_code == 404
    assert response.json['message'] == "A note with the given ID does not exist"
    

    # Truncate all database tables
    truncate_db()
