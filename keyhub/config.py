import os

DEBUG = bool(os.environ.get("DEBUG", 0))
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///keyhub.db")
SQLALCHEMY_ECHO = DEBUG
