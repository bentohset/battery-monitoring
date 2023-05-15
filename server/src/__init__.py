from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    cors = CORS(app)

    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Battery, TimeSeriesData

    with app.app_context():
        db.create_all()



    return app

def create_database(app):
    if not path.exists('src/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')