from flask import Blueprint, jsonify
from system.LogManager import LogManager

defi = Blueprint('v1_index_api', __name__)

@defi.route('/', methods=['GET'])
def index_page():
    access_log = LogManager.get_logger('access_log', LogManager.LOG_INFO)
    access_log.write('Access index page', LogManager.LOG_INFO)
    return jsonify(status=200, msg={
        "message": "Server is running. This is version 1 API."
    })