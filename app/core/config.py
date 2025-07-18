"""
Configuration classes for different environments.
Manages database URIs, debug settings, and environment-specific settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    DEBUG = True     # Enables debug mode, reloader, detailed error pages
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URI",
        "postgresql://user:password@localhost:5432/dbname"
    )

class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")

class TestConfig(BaseConfig):
    TESTING = True  # Enables testing behaviors in Flask (eg, suppress error catching)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URI",
        "postgresql://user:password@localhost:5432/test_dbname"
    )
    # Future testing options to look into:
    # WTF_CSRF_ENABLED = False  # Disable CSRF for form testing
    # DEBUG = False             # Optional: Disable debug in tests

config_map = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "testing": TestConfig,
}