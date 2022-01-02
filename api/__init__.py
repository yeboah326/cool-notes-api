from flask import Flask
from .config import config_dict
import os
from dotenv import load_dotenv
from .extensions import *

# Load environment variables
load_dotenv()

def create_app() -> Flask:
    app = Flask(__name__)
    
    # Initial project configurations
    env = os.getenv("FLASK_ENV")
    app.config.from_object(f"api.config.{config_dict[env]}")

    # Loading app extensions
    db.init_app(app)
    migrate.init_app(app,db)
    cors.init_app(app)
    jwt.init_app(app)

    # Loading app blueprints
    from api.account.controllers import account
    from api.note.controllers import note
    from api.tag.controllers import tag


    return app