import os 
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "AFLLG")
    SQLALCHEMY-TRACK-MODIFICATION = False

class DevConfig(Config):
    DEBUG = os.getenv("DEBUG", "True") == "True"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///recipes.db")

class TestConfig(Config):
    """Testing configuration (pytest)."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProdConfig(Config):
    DEBUG = os.getenv("DEBUG", "FALSE") == "FALSE"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    