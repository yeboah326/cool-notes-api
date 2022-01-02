import os
from datetime import timedelta

class BaseConfig:
    JWT_SECRET_KEY = "69ee1a6bbc7e77e347ebbd7c802c0c72beb10a7e747e2ca92704e31231bcd8de"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)

class ProductionConfig(BaseConfig):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)

class DevelopmentConfig(BaseConfig):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    

config_dict = {"production": "ProductionConfig", "development": "DevelopmentConfig"}