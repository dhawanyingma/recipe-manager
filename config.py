import os 
from dotenv import load_dotenv

#load environment variables from .env if present
load_dotenv()

#Base directory of the project(absolute path)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "AFLLG")
    SQLALCHEMY_TRACK_MODIFICATION = False

class DevConfig(Config):
    DEBUG = os.getenv("DEBUG", "True") == "True"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(BASE_DIR, 'recipes.db')}"
        )

class TestConfig(Config):
    """Testing configuration (pytest)."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProdConfig(Config):
    DEBUG = os.getenv("DEBUG", "FALSE") == "FALSE"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    