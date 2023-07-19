"""Configure environment variables from .env file according to environment"""

from os import path, environ
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config(object):
    """
    Base class for all config environments
    """

    FLASK_APP = "app.py"
    DEBUG = True
    SECRET_KEY = environ.get("SECRET_KEY")
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    PASSWORD_RESET_SECRET = environ.get("PASSWORD_RESET_SECRET")
    

class ProductionConfig(Config):
    """
    Class inherited from Base config for Production
    Set Database URI for prod
    """

    FLASK_ENV = "production"
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ""
    DEBUG = False

class DevelopmentConfig(Config):
    """
    Class inherited from Base config for Development
    Database URI for development on LAN remote server 
    """

    FLASK_ENV = "development"
    TESTING = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    DEVELOPMENT = True

class TestingConfig(Config):
    """
    Class inherited from Base config for Testing
    Testing is true
    Database URI uses SQLite connecting to instance/testdb.db
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get("TEST_DATABASE_URL")
