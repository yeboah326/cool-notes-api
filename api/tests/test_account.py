from api.tests.setup import truncate_db
from api.tests.setup import create_user


def test_account_create_successful(client):
    # Drop database
    truncate_db()

    response = client.post(
        "/api/account/",
        json={
            "name": "John Doe",
            "email": "jdoe@gmail.com",
            "password": "123456789",
            "account_type": "normal",
        },
    )

    assert response.status_code == 200
    assert response.json["message"] == f"User account for John Doe created successfully"

    # Drop database
    truncate_db()


def test_account_create_error(client):
    # Drop database
    truncate_db()

    response = client.post(
        "/api/account/",
        json={"name": "John Doe", "email": "jdoe@gmail.com", "password": "123456789"},
    )

    assert response.status_code == 422
    assert response.json["errors"] == {
        "account_type": ["Missing data for required field."]
    }
    assert response.json["message"] == "Invalid data"

    # Drop database
    truncate_db()


def test_account_authenticate_successful(client):
    # Drop database
    truncate_db()

    user = create_user(client)

    response = client.post(
        "/api/account/auth", json={"email": "jdoe@gmail.com", "password": "123456789"}
    )
    assert response.json["token"]
    assert response.json["account"]["name"] == "John Doe"
    assert response.json["account"]["account_type"] == "normal"

    # Drop database
    truncate_db()


def test_account_authenticate_wrong_credentials(client):
    # Drop database
    truncate_db()

    user = create_user(client)

    response = client.post(
        "/api/account/auth", json={"email": "jdoe@gmail.com", "password": "1234567890"}
    )

    assert response.status_code == 400
    assert response.json["message"] == "Either the username or password is invalid"

    # Drop database
    truncate_db()


def test_account_authenticate_errors(client):
    # Drop database
    truncate_db()

    user = create_user(client)

    response = client.post("/api/account/auth", json={"email": "jdoe@gmail.com"})

    assert response.status_code == 422
    assert response.json["message"] == "Invalid data"

    # Drop database
    truncate_db()
