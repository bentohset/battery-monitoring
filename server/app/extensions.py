from flask_sqlalchemy import SQLAlchemy
from flask_mailman import Mail

"""
All app extensions here
"""

db = SQLAlchemy()
mail = Mail()
