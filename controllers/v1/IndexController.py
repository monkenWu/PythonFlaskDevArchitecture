from flask import Blueprint, jsonify

defi = Blueprint('v1_index_api', __name__)

@defi.route('/', methods=['GET'])
def index_page():
    return jsonify(status=200, msg={
        "message": "Server is running. This is version 1 API."
    })