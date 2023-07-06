from app.main import bp
from flask import jsonify
from app.common import status

@bp.route('/')
def health():
    return jsonify(dict(status="OK")), status.HTTP_200_OK