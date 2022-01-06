from .setup import *
from api.tag.models import Tag
from api.tag.schemas import *


def test_tag_create_successful(client):
    # Drop database
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    response = client.post(
        "/api/tag/",
        json={"name": "food"},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    tag = tag_schema.dump(Tag.query.filter_by(name="food").first())

    assert response.status_code == 200
    assert response.json["message"] == "food created successfully"
    assert tag["name"] == "food"
    assert tag["author_id"] == user["account"]["id"]

    # Drop database
    truncate_db()


def test_tag_create_error(client):
    # Drop database
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    response = client.post(
        "/api/tag/",
        json={},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    assert response.status_code == 400
    assert response.json["message"] == "Invalid data"
    assert response.json["errors"] == {"name": ["Missing data for required field."]}

    # Drop database
    truncate_db()


def test_tag_delete_by_id_successful(client):
    # Drop database
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a tag for testing
    tag = create_tag(client, user)

    response = client.delete(
        f"/api/tag/{tag['id']}", headers={"Authorization": f"Bearer {user['token']}"}
    )

    # Find deleted tag
    deleted_tag = tag_schema.dump(Tag.find_by_id(tag["id"]))

    assert response.status_code == 200
    assert response.json["message"] == "Tag deleted successfully"
    assert deleted_tag == {}

    # Drop database
    truncate_db()


def test_tag_delete_by_id_not_exist(client):
    # Drop database
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a tag for testing
    tag = create_tag(client, user)

    response = client.delete(
        f"/api/tag/{tag['id'] + 1}",
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "A tag with the given ID does not exist"

    # Drop database
    truncate_db()


def test_tag_update_by_id_successful(client):
    # Drop database
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a tag for testing
    tag = create_tag(client, user)

    response = client.put(
        f"/api/tag/{tag['id']}",
        json={"new_name": "tech"},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    # Find modified tag
    modified_tag = tag_schema.dump(Tag.find_by_id(tag["id"]))

    assert response.status_code == 200
    assert response.json["message"] == "Tag updated successfully"
    assert modified_tag["name"] == "tech"
    assert modified_tag["author_id"] == user["account"]["id"]

    # Drop database
    truncate_db()


def test_tag_update_by_id_not_exist(client):
    # Drop database
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a tag for testing
    tag = create_tag(client, user)

    response = client.put(
        f"/api/tag/{tag['id'] + 1}",
        json={"new_name": "tech"},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    # Find modified tag
    modified_tag = tag_schema.dump(Tag.find_by_id(tag["id"] + 1))

    assert response.status_code == 404
    assert response.json["message"] == "A tag with the given ID does not exist"
    assert modified_tag == {}

    # Drop database
    truncate_db()


def test_tag_get_by_id_successful(client):
    # Drop database
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a tag for testing
    tag = create_tag(client, user)

    response = client.get(
        f"/api/tag/{tag['id']}", headers={"Authorization": f"Bearer {user['token']}"}
    )

    assert response.status_code == 200
    assert response.json["tag"]["name"] == "food"
    assert response.json["tag"]["author_id"] == user["account"]["id"]

    # Drop database
    truncate_db()


def test_tag_get_by_id_not_exist(client):
    # Drop database
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a tag for testing
    tag = create_tag(client, user)

    response = client.get(
        f"/api/tag/{tag['id'] + 1}",
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "A tag with the given ID does not exist"

    # Drop database
    truncate_db()


def test_tag_get_all_successful(client):
    # Drop database
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a tag for testing
    tags = create_multiple_tags(client, user)

    response = client.get(
        "api/tag/", headers={"Authorization": f"Bearer {user['token']}"}
    )

    assert response.status_code == 200
    assert len(response.json["tags"]) == 3
    assert response.json["tags"][0]["name"] == "food0"
    assert response.json["tags"][1]["name"] == "food1"
    assert response.json["tags"][2]["name"] == "food2"

    # Drop database
    truncate_db()


def test_tag_add_to_note_successful(client):
    # Drop database
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a tag for testing
    tag = create_tag(client, user)

    # Create a new note for testing
    note = create_note(client, user["token"])

    response = client.post(
        "api/tag/add_tag",
        json={"note_id": note["id"], "tag_id": tag["id"]},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Tag added to note successfully"

    # Drop database
    truncate_db()


def test_tag_remove_from_note_successful(client):
    # Drop database
    truncate_db()

    # Create a user login token
    user = create_user_login_token(client)

    # Create a note with a tag
    tagged_note = create_note_with_tag(client, user)

    response = client.post(
        "api/tag/remove_tag",
        json={"note_id": tagged_note.note_id, "tag_id": tagged_note.tag_id},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Tag removed from note successfully"

    # Drop database
    truncate_db()
