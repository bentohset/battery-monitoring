from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import INTEGER, BOOLEAN, CITEXT, VARCHAR

from . import db

class Battery(db.Model):
    __tablename__ = "batteries"

    id = db.Column(db.Integer, primary_key=True)
    shelf_id = db.Column(db.Integer)
    container_id = db.Column(db.Integer)
    # init method if any field needs to be set to initial value


# | id | battery_id(int) | ble_uuid(int) | humidity(numeric/decimal) | temperature(numeric) 
# | voltage_open_circuit(numeric) | internal_series_resistance(numeric) | internal_impedance(numeric) | 
class TimeSeriesData(db.Model):
    __tablename__ = "readings"

    id = db.Column(db.Integer, primary_key=True)
    battery_id = db.Column(db.Integer, db.ForeignKey('batteries.id'))
    battery = db.relationship('Battery', backref=db.backref('readings', lazy=True))
    ble_uuid = db.Column(db.String(255), nullable=False)
    humidity = db.Column(db.Float)
    temperature = db.Column(db.Float)
    voltage_open_circuit = db.Column(db.Float)
    internal_series_resistance = db.Column(db.Float)
    internal_impedance = db.Column(db.Float)
    timestamp = db.Column(db.TIMESTAMP) # recorded every few hours
    
    
# | id(int) | email(citext) | password(varchar) | is_requesting_resest(boolean)
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False) # hashed   
    is_requesting_reset = db.Column(db.Boolean, nullable=False, default=False)
