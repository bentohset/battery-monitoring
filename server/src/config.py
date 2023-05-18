from os import path, environ
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))



class Config(object):
    FLASK_APP = "app.py"
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SECRET_KEY = environ.get("SECRET_KEY")
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    PASSWORD_RESET_SECRET = environ.get("PASSWORD_RESET_SECRET")
    

class ProductionConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False

class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    ENV = "development"
    DEVELOPMENT = True
