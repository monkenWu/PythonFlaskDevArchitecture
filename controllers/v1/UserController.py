from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.UserService import UserService

defi = Blueprint('v1_user_api', __name__)
user_service = UserService()

@defi.route('/user', methods=['POST'])
def register():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({"msg": "The 'username' or 'password' not found"}), 400
    user = user_service.register(data['username'], data['password'])
    if user:
        return jsonify({"msg": "User created", "user": {"username": user.username}}), 201
    else:
        return jsonify({"msg": "User already exists"}), 409

@defi.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({"msg": "The 'username' or 'password' not found"}), 400
    access_token = user_service.login(data['username'], data['password'])
    if access_token:
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@defi.route('/user', methods=['GET'])
@jwt_required()
def get_info():
    user_info = user_service.get_user_info(UserService.get_current_user_name())
    if user_info:
        return jsonify(user_info), 200
    else:
        return jsonify({"msg": "User not found"}), 404
