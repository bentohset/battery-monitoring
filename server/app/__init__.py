from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from config import DevelopmentConfig, ProductionConfig, TestingConfig
import os
from app.extensions import db, mail
from app.common import status

"""
Function which creates the app with env variables, db and extensions
Exported to and called in main process

Returns a Flask app run by main process
"""
def create_app():
    app = Flask(__name__)
    cors = CORS(app)
    
    # Init config state
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object(ProductionConfig)
    elif env == "development":
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(TestingConfig)


    # Initialize Flask extensions
    db.init_app(app)
    mail.init_app(app)


    # Register blueprints
    from app.main import bp as main_bp
    from app.auth import auth_bp
    from app.batteries import battery_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(battery_bp, url_prefix='/battery')

    @app.route("/test")
    def test():
        return jsonify({'message': 'hello backend'}), status.HTTP_200_OK

    # creates database and tables if not already existing
    with app.app_context():
        db.create_all()

    return app