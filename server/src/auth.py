# auth routes
from flask import Blueprint, current_app, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from threading import Thread
import jwt
import datetime

from . import db   ## means from __init__.py import db
from .models import User
from services.mail_service import create_email

auth = Blueprint('auth', __name__)

token_blacklist = set()

'''
Helper Functions:

require token wrapper, send email, 
get token for password reset, decode password reset token
'''
def requires_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authentication' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')
            current_user = User.query.get(data)
        except:
            return jsonify({'message': 'Token is invalid!'}), 402
        return f(current_user, *args, **kwargs)
    
    return decorated

def send_email(app, msg):
    with app.app_context():
        try:
            msg.send(fail_silently=False)
        except:
            return jsonify({'message': 'Error sending email!'}),402

def get_password_reset_token(requesting_user, expiry_delta):
    return jwt.encode(
        {
            'user_id': requesting_user,
            'exp':  datetime.datetime.utcnow() + expiry_delta
        },
        key=current_app.config['PASSWORD_RESET_SECRET'],
        algorithm="HS256"
    )

def decode_reset_token(token):
    token_data = jwt.decode(token, key=current_app.config['PASSWORD_RESET_SECRET'], algorithms='HS256')

    return token_data


'''
Login routes:

Login, register, logout, protected
'''

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
        print("user added")
        db.session.commit()
        print("session commited")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'message': 'Error occurred while registering the user.'}), 501
    
    return jsonify({'message': 'User successfully created!'}), 200




# protected route, acts as gatekeeper for resources that require auth
@auth.route('/auth/protected', methods=['GET'])
@requires_token
def protected(current_user):
    return jsonify({'message': 'Successfully logged in. Redirecting...'}), 200




"""
Forgot password route:

Prompt user for email to send password reset token
check if email exists within database
if exists, create reset token (valid for 15min) send link to user email
"""

@auth.route('/auth/forgot', methods=['POST'])
def submit_email():
    form_data = request.get_json()
    email = form_data["email"]
    print(email)

    #check if email is in db
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message":"email does not exist"}), 400
    
    #if email exists, create token with jwt and send email with token, set boolean to true
    user.is_requesting_reset = True
    db.session.commit()

    expire_time = datetime.timedelta(minutes=10)
    reset_token = get_password_reset_token(user.id, expire_time)
    print("token " + reset_token)
    print("expire time " + str(expire_time))

    # with current_app.test_request_context():
    #     url = url_for('auth.get_reset_token', token=reset_token, _external=True)
    # NOTE uncomment above for production

    url = "http://localhost:3000/auth/reset/" + reset_token     # NOTE do not use for production
    msg = create_email(email, url)

    app = current_app._get_current_object()
    thread = Thread(target=send_email, args=(app,msg))
    thread.start()

    print("message sent")
    return jsonify({"message":"Email sent!"}), 200




# check if token is valid. if valid, ask for password and update db user entry password
@auth.route('/auth/reset/<token>', methods=['GET'])
def get_reset_token(token):
    #decode token, check if expired or invalid
    decoded_token = decode_reset_token(token)
    token_userid = decoded_token['user_id']
    token_exp = decoded_token['exp']

    if token_userid is None:
        return jsonify({"message":"Token is invalid"}), 403
    if token_exp == datetime.now():
        return jsonify({"message":"Token is expired"}), 403
    
    #check if user is requesting reset
    user_requesting_reset = User.query.filter_by(id=token_userid).first()
    if user_requesting_reset.is_requesting_reset is False:
        return jsonify({"message":"User did not request for reset"}), 401

    
    return jsonify({"message":"Redirecting to password reset page"}), 200


# update password and set user requesting status as false
@auth.route('/auth/reset/<token>', methods=['POST'])
def update_password(token):
    form_data = request.get_json()
    new_password = form_data["new_password"]
    try:
        token = decode_reset_token(token)
    except jwt.exceptions.ExpiredSignatureError as ee:
        print(ee)
        return jsonify({"message":"Token is expired"}), 403
    except Exception as e:
        print(e)
        return jsonify({"message":"Token cannot be decoded"}), 403
    

    token_userid = token['user_id']
    token_exp = token['exp']
    exp_datetime = datetime.datetime.fromtimestamp(token_exp)

    if token_userid is None:
        return jsonify({"message":"Token is invalid"}), 403
    if exp_datetime < datetime.datetime.utcnow():
        return jsonify({"message":"Token is expired"}), 403
    
    #update db user entry with new password
    user_requesting_reset = User.query.filter_by(id=token_userid).first()
    if user_requesting_reset.is_requesting_reset is False:
        return jsonify({"message":"User not requesting for reset"}), 403

    user_requesting_reset.password = generate_password_hash(new_password, method='sha256')
    user_requesting_reset.is_requesting_reset = False
    db.session.commit()

    return jsonify({'message': "Password updated successfully"}), 200