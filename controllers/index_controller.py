from flask import Blueprint, jsonify

defi = Blueprint('index_api', __name__)

@defi.route('/')
def index_page():
    return jsonify(status=200, msg={
        "message": "Server is running"
    })