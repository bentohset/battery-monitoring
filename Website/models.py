from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import JSON


class Batteries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    completed=db.Column(db.Boolean)