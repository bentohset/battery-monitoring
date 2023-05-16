# auth routes
from flask import Blueprint, current_app, jsonify, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from .models import User
import jwt
from functools import wraps

auth = Blueprint('auth', __name__)

token_blacklist = set()

def requires_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authentication' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.get(data)
        except:
            return jsonify({'message': 'Token is invalid!'}), 402
        return f(current_user, *args, **kwargs)
    
    return decorated



# login
@auth.route('/auth/login', methods=['POST'])
def login():
    form_data = request.get_json()
    email = form_data["email"]
    password = form_data["password"]
    print("email " + email)
    print("password " + password)

    
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            # correct, authenticate and get token
            print("successful login")
            token = jwt.encode({
                'id':user.id
            }, current_app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'token': token}), 200
        else: 
            return jsonify({'message': 'Invalid password'}), 403
        
    else:
        return jsonify({'message': 'Invalid email'}), 403


    return jsonify({'message': 'Unhandled exception. Will never reach here'}), 403



# logout
@auth.route('/auth/logout')
@requires_token
def logout():
    # client side: remove token from cache and reset user session data
    # server: extract token and add to blacklist
    token = request.headers['Authorization'].split()[1]
    token_blacklist.add(token)

    return jsonify({'message': 'You have been successfully logged out'}), 200



# register
@auth.route('/auth/register', methods=['POST'])
def register():
    form_data = request.get_json()
    email = form_data["email"]
    password = form_data["password"]
    # print("email " + email)
    # print("password " + password)

    user = User.query.filter_by(email=email).first() # checks if user already exists

    if user != None:
        return jsonify({'message': 'User already exists'}), 401
    # other string manipulation checks should be done on client side
    
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
    print("user generated")
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'Error occurred while registering the user.'}), 501
    
    return jsonify({'message': 'User successfully created!'}), 200

# forgot password/email
