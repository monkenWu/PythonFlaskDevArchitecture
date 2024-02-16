from flask import Blueprint, jsonify

defi = Blueprint('v1_user_api', __name__)

@defi.route('/user', methods=['GET'])
def index_page():
    return jsonify(status=200, msg={
        "message": "Server is running"
    })