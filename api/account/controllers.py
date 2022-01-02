from flask import Blueprint
from api.account.models import Account
from flask_jwt_extended import jwt_required

account = Blueprint("account",__name__, url_prefix="api/account")

# TODO: Create user endpoint
@account.post("/")
def account_create():
    pass

# TODO: Authenticate user endpoint
@account.get("/auth")
def account_authenticate():
    pass


# TODO: Read all users endpoint (protected)
@account.get("/")
@jwt_required()
def account_get_all():
    pass

