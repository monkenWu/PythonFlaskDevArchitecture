from model.TaskDAO import TaskDAO
from system.Exceptions import ValidationError

class TaskService:
    def __init__(self):
        self.task_dao = TaskDAO()

    def create_task(self, user_id, name):
        task = self.task_dao.find_by_name(user_id, name)
        if task:
            raise ValidationError(f'Task {name} already exists')

        return self.task_dao.create_task(user_id, name)

    def get_tasks(self, user_id):
        return self.task_dao.get_all_tasks_for_user(user_id)

    def update_task(self, user_id, task_id, name, status):
        task = self.task_dao.find_by_id(user_id, task_id)
        if not task:
            raise ValidationError(f'Task {task_id} not found')
        if name is "":
            raise ValidationError("The 'name' don't be empty")
        if status not in [0, 1]:
            raise ValidationError("The 'status' must be 0 or 1")
        
        duplicate_task = self.task_dao.find_by_name(user_id, name)
        if duplicate_task and duplicate_task.id != task_id:
            raise ValidationError(f'Task {name} already exists')

        return self.task_dao.update_task(user_id, task_id, name=name, status=status)
    
    def patch_task(self, user_id, task_id, **kwargs):

        if 'name' in kwargs and kwargs['name'] == "":
            raise ValidationError("The 'name' don't be empty")

        if 'status' in kwargs and kwargs['status'] not in [0, 1]:
            raise ValidationError("The 'status' must be 0 or 1")
        
        if 'name' in kwargs:
            duplicate_task = self.task_dao.find_by_name(user_id, kwargs['name'])
            if duplicate_task and duplicate_task.id != task_id:
                raise ValidationError(f'Task {kwargs["name"]} already exists')

        return self.task_dao.update_task(user_id, task_id, **kwargs)

    def delete_task(self, user_id, task_id):
        return self.task_dao.delete_task(user_id, task_id)
