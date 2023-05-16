from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from os import path
from datetime import datetime

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    cors = CORS(app)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .auth import auth
    from .routes import routes

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')

    from .models import User, Battery, TimeSeriesData

    with app.app_context():
        db.create_all()
        # x=TimeSeriesData(id=1,battery_id=1,timestamp=datetime.now(),impedance=1.0,temperature=2.0,humidity=4.0)
        # db.session.add(x)
        # db.session.commit()

    return app

def create_database(app):
    if not path.exists('src/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')