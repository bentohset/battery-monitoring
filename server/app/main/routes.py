from app.main import bp
from flask import jsonify
from app.common import status


# 
@bp.route('/')
def health():
    """
    Signals the health of the server
    Always returns 200 OK

    Returns:
        list: status=OK
    
    """
    return jsonify(dict(status="OK")), status.HTTP_200_OK