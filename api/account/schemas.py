from api.account.models import Account
from marshmallow import Schema, fields, post_load, post_dump

class AccountSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    date_created = fields.Str(required=True, dump_only=True)
    date_updated = fields.DateTime(required=True, dump_only=True)
    account_type = fields.Str(required=True)

    @post_load
    def create_account(self, data, **kwargs):
        return Account(**data)

account_schema = AccountSchema(unknown="EXCLUDE")
accounts_schema = AccountSchema(many=True, unknown="EXCLUDE")

class AccountLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @post_load
    def return_account(self, data, **kwargs):
        return Account.find_by_email(data["email"])

account_login_schema = AccountLoginSchema(unknown="EXCLUDE")