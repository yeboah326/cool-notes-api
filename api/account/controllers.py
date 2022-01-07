from flask import Blueprint, request, jsonify
from api.extensions import db
from api.account.models import Account
from api.account.schemas import *
from api.account.utils import check_super_status
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from marshmallow.exceptions import ValidationError

account = Blueprint("account",__name__, url_prefix="/api/account")

@account.post("/")
def account_create():
    """
    name, email, password
    """
    # Retrieve the incoming data
    data = request.get_json()

    try:
        account = Account.find_by_email(data['email'])
        if account:
            return {"message": "A user with the given email exists"}, 400
        # Create the account instance
        new_account = account_schema.load(data)
        new_account.password = data["password"]

        # Add to the database
        db.session.add(new_account)
        db.session.commit()

        return {"message": f"User account for {data['name']} created successfully"}, 200

    except ValidationError as e:
        return {"message": "Invalid data", "errors": e.messages}, 422

@account.post("/auth")
def account_authenticate():
    # Retrieve incoming data
    data = request.get_json()

    try:
        # Retrive user instance
        account = account_login_schema.load(data)

        if account:
            password_correct = account.check_password(data["password"])
            if password_correct:
                token = create_access_token(identity=account.id)
                return {"token": token, "account": account_schema.dump(account)}, 200
            return {"message": "Either the username or password is invalid"}, 400
    except ValidationError as e:
        return {"message": "Invalid data", "errors": e.messages}, 422

@account.get("/")
@jwt_required()
def account_get_all():
    if not(check_super_status(get_jwt_identity())):
        return {"message": "User not authorized to perform this action"}, 401
    accounts = accounts_schema.dump(Account.query.all())
    return {"accounts": accounts}, 200

