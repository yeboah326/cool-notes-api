from api import db
from api.account.models import Account
from api.account.schemas import account_schema

def truncate_db():
    meta = db.metadata
    for table in meta.sorted_tables[::-1]:
        db.session.execute(table.delete())
    db.session.commit()

def create_user(client):
    user_info = {"name": "John Doe", "email": "jdoe@gmail.com", "password": "123456789", "account_type":"normal"}
    client.post(
        "/api/account/",
        json=user_info,
    )
    return account_schema.dump(Account.query.filter_by(name=user_info["name"]))

