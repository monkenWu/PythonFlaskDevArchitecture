from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.TaskService import TaskService
from services.UserService import UserService
from system.Exceptions import ValidationError

defi = Blueprint('v1_task_api', __name__)
task_service = TaskService()

@defi.route('/tasks', methods=['GET'])
@jwt_required()
def list_tasks():
    user_id = UserService.get_current_user_id()
    tasks = task_service.get_tasks(user_id)
    return jsonify({
        'result': [task.to_dict() for task in tasks]
    }), 200

@defi.route('/task', methods=['POST'])
@jwt_required()
def create_task():
    user_id = UserService.get_current_user_id()
    data = request.get_json()
    if 'name' not in data:
        raise ValidationError("The 'name' not found")
    task = task_service.create_task(user_id, data['name'])
    return jsonify({
        'result': {
            "name" : task.name,
            "status" : task.status,
            "id" : task.id
        }
    }), 201

@defi.route('/task/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = UserService.get_current_user_id()
    data = request.get_json()
    for key in ['name', 'status']:
        if key not in data:
            raise ValidationError(f"The '{key}' not found")
    task = task_service.update_task(user_id, task_id, data['name'], data['status'])
    if task:
        return jsonify(task.to_dict()), 200
    else:
        raise ValidationError('Task not found or update failed')

@defi.route('/task/<int:task_id>', methods=['PATCH'])
@jwt_required()
def patch_task(task_id):
    user_id = UserService.get_current_user_id()
    data = request.get_json()

    if not data:
        raise ValidationError("The request body is empty")

    task = task_service.patch_task(user_id, task_id, **data)
    if task:
        return jsonify(task.to_dict()), 200
    else:
        raise ValidationError('Task not found or update failed')

@defi.route('/task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = UserService.get_current_user_id()
    task_service.delete_task(user_id, task_id)
    return '', 200
