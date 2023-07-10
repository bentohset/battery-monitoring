from flask import Blueprint

battery_bp = Blueprint('battery', __name__)

from app.batteries import routes