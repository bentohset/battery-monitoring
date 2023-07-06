from flask import Blueprint

bp = Blueprint('battery', __name__)

from app.batteries import routes