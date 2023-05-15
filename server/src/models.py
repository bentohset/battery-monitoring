from flask_sqlalchemy import SQLAlchemy
from . import db

class Battery(db.Model):
    __tablename__ = "batteries"

    id = db.Column(db.Integer, primary_key=True)
    shelf_id = db.Column(db.Integer)
    container_id = db.Column(db.Integer)
    # init method if any field needs to be set to initial value
    
class TimeSeriesData(db.Model):
    __tablename__ = "readings"

    id = db.Column(db.Integer, primary_key=True)
    battery_id = db.Column(db.Integer, db.ForeignKey('batteries.id'))
    battery = db.relationship('Battery', backref=db.backref('readings', lazy=True))
    timestamp = db.Column(db.TIMESTAMP) # recorded every few hours
    impedance = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # hashed