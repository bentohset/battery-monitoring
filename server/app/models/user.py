from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False) # hashed   
    is_requesting_reset = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email:str, password_str:str):
        """Creates a user instance and hashes the plaintext password"""

        self.email = email
        self.password = self._generate_password_hash(password_str)
    
    def is_password_correct(self, password_str:str):
        """Checks if password provided is correct"""

        return check_password_hash(self.password, password_str)

    def set_password(self, password_str:str):
        """Sets user password as new hashed password"""

        self.password = self._generate_password_hash(password_str)

    @staticmethod
    def _generate_password_hash(password_str):
        """Static method to generate password hash"""
        
        return generate_password_hash(password_str)