from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_mailman import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    cors = CORS(app)

    app.config.from_object('src.config.DevelopmentConfig')      # change to ProductionConfig for prod
    
    db.init_app(app)
    mail.init_app(app)

    from .auth import auth
    from .routes import routes

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')

    from .models import User, Battery, TimeSeriesData

    with app.app_context():
        db.create_all()

    return app