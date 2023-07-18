from flask import current_app, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from threading import Thread
import jwt
import datetime
from flask_jwt_extended import unset_jwt_cookies
from flask_mailman import EmailMessage

from app.auth import auth_bp
from app.extensions import db
from app.common import status

from app.models.user import User

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
            return jsonify({'message': 'Token is missing!'}), status.HTTP_401_UNAUTHORIZED
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')
            current_user = User.query.get(data)
        except:
            return jsonify({'message': 'Token is invalid!'}), status.HTTP_403_FORBIDDEN
        return f(current_user, *args, **kwargs)
    
    return decorated

def create_email(email, url):
    msg = EmailMessage()
    msg.subject = "Password Reset"
    msg.from_email = 'bentohdev@gmail.com'
    msg.to = [email]
    msg.body = f'''To reset your password, please visit this URL:\n 
            
    {url}\n

    If you didn't request for a password reset, please ignore this message.
    
    '''
    
    return msg

# sends the email with the password reset link
def send_email(app, msg):
    with app.app_context():
        try:
            msg.send(fail_silently=False)
        except:
            return jsonify({'message': 'Error sending email!'}), status.HTTP_408_REQUEST_TIMEOUT

# generates the password reset token using JWT with user_id and expiry time
def get_password_reset_token(requesting_user, expiry_delta):
    return jwt.encode(
        {
            'user_id': requesting_user,
            'exp':  datetime.datetime.utcnow() + expiry_delta
        },
        key=current_app.config['PASSWORD_RESET_SECRET'],
        algorithm="HS256"
    )

# decodes the password reset JWT token with the key and returns the decoded data
def decode_reset_token(token):
    token_data = jwt.decode(token, key=current_app.config['PASSWORD_RESET_SECRET'], algorithms='HS256')

    return token_data


'''
Login routes:

Login, register, logout, protected
'''

# login
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login route

    Given email and password string from request, searches for a user and checks if the hashed password is correct

    Returns:
        JWT encoded with user_id
    
    Raises:
        404 Not Found: user does not exist within the DB
        401 Unauthorized: invalid password provided
        400 Bad Request: Unhandled exception which will never be executed
    """

    form_data = request.get_json()
    email = form_data["email"]
    password = form_data["password"]
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Invalid email'}), status.HTTP_404_NOT_FOUND
    
    if user.is_password_correct(password):
        token = jwt.encode({
            'id':user.id
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token}), status.HTTP_201_CREATED
    else: 
        return jsonify({'message': 'Invalid password'}), status.HTTP_401_UNAUTHORIZED
    

    return jsonify({'message': 'Unhandled exception. Will never reach here'}), status.HTTP_400_BAD_REQUEST



# logout
@auth_bp.route('/logout')
@requires_token
def logout():
    """
    Logout route
    Retrieves the token and blacklists it

    Returns:
        message of logout success
    """
    # client side: remove token from cache and reset user session data
    # server: extract token and add to blacklist
    token = request.headers['Authorization'].split()[1]
    token_blacklist.add(token)
    response = jsonify({'message': 'logout successful'})

    return response, status.HTTP_200_OK



# register
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register user route
    
    Retrieves email and password string from request, checks if user already exists and creates a new user and JWT

    Returns:
        JWT encoded with new user ID

    Raises:
        409 Conflict: User with user ID already exists within DB
        503 Service Unavailable: Error commiting new user to database
    """

    form_data = request.get_json()
    email = form_data["email"]
    password = form_data["password"]
    # print("email " + email)
    # print("password " + password)

    user = User.query.filter_by(email=email).first() # checks if user already exists

    if user != None:
        return jsonify({'message': 'User already exists'}), status.HTTP_409_CONFLICT
    # other string manipulation checks should be done on client side
    
    new_user = User(email=email, password_str=password)
    token = jwt.encode({
            'id':new_user.id
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    try:
        db.session.add(new_user)
        print("user added")
        db.session.commit()
        print("session commited")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'message': 'Error occurred while registering the user.'}), status.HTTP_503_SERVICE_UNAVAILABLE
    
    return jsonify({'token': token}), status.HTTP_201_CREATED




# protected route, acts as gatekeeper for resources that require auth
@auth_bp.route('/auth/protected', methods=['GET'])
@requires_token
def protected(current_user):
    return jsonify({'message': 'Successfully logged in. Redirecting...'}), status.HTTP_200_OK




"""
Forgot password route:

Prompt user for email to send password reset token
check if email exists within database
if exists, create reset token (valid for 15min) send link to user email
"""


@auth_bp.route('/forgot', methods=['POST'])
def submit_email():
    """
    Sends the email upon request from user

    Given the email from request, validate if it exists within the database and sends the email template with the reset_token url
    which leads to a frontend site

    Returns:
        object with message email sent

    Raises:
        404 Not Found: if email provided does not exist
        408 Timed Out: if email sender fails to send email
    """

    form_data = request.get_json()
    email = form_data["email"]
    print(email)

    #check if email is in db
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message":"email does not exist"}), status.HTTP_404_NOT_FOUND
    
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
    thread.join()
    return jsonify({"message":"Email sent!"}), status.HTTP_200_OK




# check if token is valid. if valid, ask for password and update db user entry password
@auth_bp.route('/reset/<token>', methods=['GET'])
def get_reset_token(token):
    """
    Checks if a reset session is valid

    Given the JWT, decode it which provides the user ID and expiry date.
    Validates the JWT and checks if user is requesting for reset.
    
    Args:
        token: JWT encoded token

    Returns:
        object with message to redirect to reset password page

    Raises:
        403 Forbidden: if token is expired or not a valid JWT when decoding
        401 Unauthorized: if user is_requesting_reset is not true when user requests for reset
    """

    #decode token, check if expired or invalid
    decoded_token = decode_reset_token(token)
    token_userid = decoded_token['user_id']
    token_exp = decoded_token['exp']

    if token_userid is None:
        return jsonify({"message":"Token is invalid"}), status.HTTP_403_FORBIDDEN
    if token_exp == datetime.now():
        return jsonify({"message":"Token is expired"}), status.HTTP_403_FORBIDDEN
    
    #check if user is requesting reset
    user_requesting_reset = User.query.filter_by(id=token_userid).first()
    if user_requesting_reset.is_requesting_reset is False:
        return jsonify({"message":"User did not request for reset"}), status.HTTP_401_UNAUTHORIZED

    
    return jsonify({"message":"Redirecting to password reset page"}), status.HTTP_200_OK


# update password and set user requesting status as false
@auth_bp.route('/reset/<token>', methods=['POST'])
def update_password(token):
    """
    Updates password
    
    Given the token and new password, decode the reset token. Checks if token is valid and user is requesting for reset.
    Updates the password with the new given password with respect to user ID decoded from JWT

    Args:
        token: Decoded JWT string

    Returns:
        object with message success

    Raises:
        403 Forbidden: if JWT has expired signature ExpiredSignatureError 
            or if decoded token does not have expected fields
            or if user is_requesting_reset is not true
        400 Bad Request: JWT cannot be decoded, not in the valid JWT format
    """
    
    form_data = request.get_json()
    new_password = form_data["new_password"]
    try:
        token = decode_reset_token(token)
    except jwt.exceptions.ExpiredSignatureError as ee:
        print(ee)
        return jsonify({"message":"Token is expired"}), status.HTTP_403_FORBIDDEN
    except Exception as e:
        print(e)
        return jsonify({"message":"Token cannot be decoded"}), status.HTTP_400_BAD_REQUEST
    

    token_userid = token['user_id']
    token_exp = token['exp']
    exp_datetime = datetime.datetime.fromtimestamp(token_exp)

    if token_userid is None:
        return jsonify({"message":"Token is invalid"}), status.HTTP_403_FORBIDDEN
    if exp_datetime < datetime.datetime.utcnow():
        return jsonify({"message":"Token is expired"}), status.HTTP_403_FORBIDDEN
    
    #update db user entry with new password
    user_requesting_reset = User.query.filter_by(id=token_userid).first()
    if user_requesting_reset.is_requesting_reset is False:
        return jsonify({"message":"User not requesting for reset"}), status.HTTP_403_FORBIDDEN

    user_requesting_reset.password = generate_password_hash(new_password, method='sha256')
    user_requesting_reset.is_requesting_reset = False
    db.session.commit()

    return jsonify({'message': "Password updated successfully"}), status.HTTP_200_OK